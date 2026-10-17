#!/usr/bin/env python3
"""Generate three summary charts for the README from the archived result files.

Reads (read-only, relative to the repository root):
  z32_checkpoint/methods/methods_results.json          stored M0-M5 accuracies (tuning, validation, all)
  z32_checkpoint/methods/methods_scores.npz            340 x 63 key-glyph score matrices, M0-M5
  z32_checkpoint/artifacts/trans_values_rowmajor.json  reading position k -> grid cell (row-major index)
  z32_checkpoint/full63/full63_keyids.json             the 63 key-glyph identifiers
  z32_checkpoint/artifacts/compare_z340_v4.json        reference plaintext letters (340)

Writes (into this folder, assets/):
  m0_m5_letter_agreement.png        accuracy comparison, M0-M5
  error_rank_distribution.png       rank of the correct letter's best glyph, among errors
  wilson_confidence_intervals.png   Wilson 95% intervals, tuning vs held-out validation
  chart_data.json                   every plotted number, its equation, and the SHA-256 of each input and output

Definitions
  Letter agreement at position k: the top-scoring key glyph for the cell of position k has the reference letter at k.
  Wilson 95% interval: centre = (p + z^2/(2n)) / (1 + z^2/n);
                       half-width = z * sqrt(p(1-p)/n + z^2/(4n^2)) / (1 + z^2/n);  z = 1.96.
  Error rank: 1-based position, in descending score order, of the best key glyph whose letter equals the reference letter.
  Majority-letter baseline: accuracy of always predicting the most frequent reference letter.

The script stops with an error if any recomputed number differs from the archived results.
Requires: numpy, pandas, matplotlib, seaborn (see requirements.txt).
"""
import collections
import hashlib
import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INPUTS = {
    "methods_results": ROOT / "z32_checkpoint/methods/methods_results.json",
    "scores": ROOT / "z32_checkpoint/methods/methods_scores.npz",
    "reading_order": ROOT / "z32_checkpoint/artifacts/trans_values_rowmajor.json",
    "keyids": ROOT / "z32_checkpoint/full63/full63_keyids.json",
    "reference": ROOT / "z32_checkpoint/artifacts/compare_z340_v4.json",
}
METHODS = ["M0", "M1", "M2", "M3", "M4", "M5"]
SELECTED = "M5"
N_POS = 340
SPLIT = 170          # tuning: k < 170 ; validation: k >= 170
Z = 1.96
TARGET = 0.70        # exploratory target, not a success threshold
BINS = ["2–5", "6–10", ">10"]

# dark theme (GitHub-dark palette)
BG, PANEL, GRID, TEXT, MUTED = "#0D1117", "#161B22", "#30363D", "#E6EDF3", "#8B949E"
AMBER, BLUE, GREEN = "#D29922", "#58A6FF", "#3FB950"
METHOD_COLORS = {"M0": "#8B949E", "M1": "#39C5CF", "M2": "#F85149",
                 "M3": "#A371F7", "M4": "#D29922", "M5": "#3FB950"}
SUBSET_COLORS = {"tuning (k<170)": BLUE, "validation (k≥170)": GREEN, "all 340": MUTED}
BIN_COLORS = {"2–5": "#39C5CF", "6–10": "#A371F7", ">10": "#F778BA"}
THEME = {
    "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG,
    "axes.edgecolor": GRID, "axes.labelcolor": TEXT, "axes.titlecolor": TEXT,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": TEXT, "grid.color": GRID,
    "font.family": "DejaVu Sans", "legend.facecolor": PANEL, "legend.edgecolor": GRID,
    "legend.labelcolor": TEXT,
}
FOOTNOTE = ("Letter agreement is position-wise agreement with the reference plaintext; it is not a full decryption. "
            "No manual visual corrections are included.")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def wilson(successes, n, z=Z):
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return centre - half, centre + half


def bin_of(rank):
    if 2 <= rank <= 5:
        return "2–5"
    if 6 <= rank <= 10:
        return "6–10"
    return ">10"


def analyse():
    results = json.loads(INPUTS["methods_results"].read_text(encoding="utf-8"))["results"]
    scores = np.load(INPUTS["scores"])
    order = json.loads(INPUTS["reading_order"].read_text(encoding="utf-8"))["values"]
    keyids = json.loads(INPUTS["keyids"].read_text(encoding="utf-8"))
    ref = json.loads(INPUTS["reference"].read_text(encoding="utf-8"))["ref"]
    assert len(order) == N_POS and len(ref) == N_POS and len(keyids) == 63

    cell_of = {value: p for p, value in enumerate(order)}
    letters = [kid[0] for kid in keyids]
    per = {}
    for m in METHODS:
        S = scores[m]
        assert S.shape == (N_POS, 63), (m, S.shape)
        correct = np.zeros(N_POS, dtype=bool)
        bins_all, bins_val = collections.Counter(), collections.Counter()
        for k in range(N_POS):
            s = S[cell_of[k]]
            correct[k] = letters[int(np.argmax(s))] == ref[k]
            if correct[k]:
                continue
            desc = np.argsort(-s, kind="stable")
            rank_of = np.empty(63, dtype=int)
            rank_of[desc] = np.arange(1, 64)
            best = min(int(rank_of[i]) for i in range(63) if letters[i] == ref[k])
            bins_all[bin_of(best)] += 1
            if k >= SPLIT:
                bins_val[bin_of(best)] += 1
        hits = {"tuning": int(correct[:SPLIT].sum()), "validation": int(correct[SPLIT:].sum()),
                "all": int(correct.sum())}
        n = {"tuning": SPLIT, "validation": N_POS - SPLIT, "all": N_POS}
        stored = results[m]
        for key, stored_key in [("tuning", "tune"), ("validation", "val"), ("all", "all")]:
            assert abs(hits[key] / n[key] - stored[stored_key]) < 1e-9, (m, key, hits[key], stored[stored_key])
        per[m] = {
            "hits": hits,
            "n": n,
            "accuracy": {key: hits[key] / n[key] for key in hits},
            "wilson95": {key: wilson(hits[key], n[key]) for key in hits},
            "errors_all": N_POS - hits["all"],
            "error_bins_validation": {b: bins_val.get(b, 0) for b in BINS},
            "error_bins_all": {b: bins_all.get(b, 0) for b in BINS},
        }
    majority_letter, majority_count = collections.Counter(ref).most_common(1)[0]
    majority = majority_count / N_POS
    sel = per[SELECTED]
    assert sel["hits"]["validation"] == 116, sel["hits"]
    assert sel["error_bins_validation"] == {"2–5": 29, "6–10": 11, ">10": 14}, sel["error_bins_validation"]
    assert per["M0"]["hits"]["all"] == 207, per["M0"]["hits"]
    return per, majority_letter, majority


def style():
    sns.set_theme(style="darkgrid", context="notebook", rc=THEME)
    plt.rcParams.update(THEME)


def save(fig, name):
    path = HERE / name
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


def chart_accuracy(per, majority):
    rows = []
    for m in METHODS:
        for label, key in [("tuning (k<170)", "tuning"), ("validation (k≥170)", "validation"), ("all 340", "all")]:
            rows.append({"method": m, "subset": label, "accuracy": per[m]["accuracy"][key]})
    df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(13.5, 7.6), layout="constrained")
    sns.barplot(data=df, x="method", y="accuracy", hue="subset", palette=SUBSET_COLORS,
                errorbar=None, edgecolor="none", width=0.8, ax=ax)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", padding=3, fontsize=8.5, color=TEXT)
    ax.axhline(TARGET, color=AMBER, ls="--", lw=1.4, zorder=0)
    ax.axhline(majority, color=MUTED, ls=":", lw=1.4, zorder=0)
    handles, labels = ax.get_legend_handles_labels()
    handles += [Line2D([0], [0], color=AMBER, ls="--", lw=1.6),
                Line2D([0], [0], color=MUTED, ls=":", lw=1.6)]
    labels += ["exploratory target 0.70 (not a success threshold)",
               f"majority-letter baseline {majority:.3f}"]
    ax.legend(handles, labels, loc="upper left", ncol=3, frameon=False)
    ax.set_xticks(range(len(METHODS)),
                  labels=[f"{m}\n(selected)" if m == SELECTED else m for m in METHODS])
    ax.set_xlabel("")
    ax.set_ylabel("letter-level agreement")
    ax.set_ylim(0, 0.9)
    fig.suptitle("Letter-level agreement with the reference plaintext, by method",
                 x=0.012, ha="left", fontsize=16, weight="bold")
    ax.set_title("Tuning (k < 170) selects the method; validation (k ≥ 170) is held out and measured once.",
                 loc="left", fontsize=10.5, color=MUTED, pad=10)
    fig.text(0.012, -0.02, FOOTNOTE, color=MUTED, fontsize=8.5)
    return save(fig, "m0_m5_letter_agreement.png")


def chart_errors(per):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 7.0), gridspec_kw={"width_ratios": [1, 1.5]},
                                   layout="constrained")
    df = pd.DataFrame({"rank bin": BINS, "errors": [per[SELECTED]["error_bins_validation"][b] for b in BINS]})
    sns.barplot(data=df, x="rank bin", y="errors", hue="rank bin", palette=[BIN_COLORS[b] for b in BINS],
                legend=False, errorbar=None, edgecolor="none", ax=ax1)
    for container in ax1.containers:
        ax1.bar_label(container, fontsize=11, padding=3, color=TEXT)
    ax1.set_title(f"{SELECTED}: held-out errors (n = {sum(per[SELECTED]['error_bins_validation'].values())})",
                  loc="left")
    ax1.set_xlabel("rank of the best correct-letter glyph (1 = top score)")
    ax1.set_ylabel("number of positions")
    x = np.arange(len(METHODS))
    bottom = np.zeros(len(METHODS))
    for b in BINS:
        vals = np.array([per[m]["error_bins_all"][b] for m in METHODS], dtype=float)
        ax2.bar(x, vals, bottom=bottom, color=BIN_COLORS[b], width=0.66, edgecolor="none", label=f"rank {b}")
        bottom += vals
    for xi, total in zip(x, bottom):
        ax2.text(xi, total + 2.5, f"{int(total)}", ha="center", color=TEXT, fontsize=10)
    ax2.set_xticks(x, labels=METHODS)
    ax2.set_xlabel("method")
    ax2.set_ylabel("algorithmic errors (of 340 positions)")
    ax2.set_title("All methods: errors over all 340 positions", loc="left")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False,
               title="rank of best correct-letter glyph")
    fig.suptitle("Where the errors fall", x=0.012, ha="left", fontsize=16, weight="bold")
    fig.text(0.012, -0.03, FOOTNOTE, color=MUTED, fontsize=8.5)
    return save(fig, "error_rank_distribution.png")


def chart_intervals(per):
    fig, ax = plt.subplots(figsize=(12.5, 7.0), layout="constrained")
    y = np.arange(len(METHODS))[::-1]
    for yi, m in zip(y, METHODS):
        v = per[m]["accuracy"]["validation"]
        lo, hi = per[m]["wilson95"]["validation"]
        ax.errorbar(v, yi, xerr=[[v - lo], [hi - v]], fmt="o", color=METHOD_COLORS[m], ms=10, lw=2.4,
                    capsize=6, zorder=4)
        ax.text(hi + 0.012, yi, f"{v:.3f}  [{lo:.3f}, {hi:.3f}]", va="center", color=TEXT, fontsize=10)
        t = per[m]["accuracy"]["tuning"]
        tlo, thi = per[m]["wilson95"]["tuning"]
        ax.errorbar(t, yi - 0.24, xerr=[[t - tlo], [thi - t]], fmt="o", mfc="none", mec=MUTED, ecolor=MUTED,
                    ms=7, lw=1.3, capsize=4, zorder=3)
    ax.axvline(TARGET, color=AMBER, ls="--", lw=1.4, zorder=1)
    ax.set_yticks(y, labels=[f"{m} (selected)" if m == SELECTED else m for m in METHODS])
    ax.set_xlim(0.40, 1.0)
    ax.set_ylim(-0.6, len(METHODS) - 0.4)
    ax.set_xlabel("letter-level agreement (Wilson 95% interval)")
    handles = [
        Line2D([0], [0], marker="o", color=MUTED, mfc=MUTED, lw=0, ms=9,
               label="validation (k ≥ 170, held out, n = 170)"),
        Line2D([0], [0], marker="o", color=MUTED, mfc="none", lw=0, ms=8,
               label="tuning (k < 170, used for selection, n = 170)"),
        Line2D([0], [0], color=AMBER, ls="--", lw=1.6, label="exploratory target 0.70"),
    ]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, 1.01), ncol=3, frameon=False)
    fig.suptitle("Wilson 95% confidence intervals: held-out validation versus tuning",
                 x=0.012, ha="left", fontsize=16, weight="bold")
    fig.text(0.012, -0.03, FOOTNOTE + " Tuning intervals are descriptive only: the method was selected on them.",
             color=MUTED, fontsize=8.5)
    return save(fig, "wilson_confidence_intervals.png")


def write_data(per, majority_letter, majority, outputs):
    doc = {
        "generator": "assets/make_charts.py",
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__,
                     "matplotlib": matplotlib.__version__, "seaborn": sns.__version__, "pandas": pd.__version__},
        "inputs": {key: {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}
                   for key, path in INPUTS.items()},
        "outputs": {path.name: {"sha256": sha256(path)} for path in outputs},
        "definitions": {
            "letter_agreement": "position k counts as correct when the top-scoring key glyph for its cell has the reference letter",
            "wilson95": "centre = (p + z^2/(2n)) / (1 + z^2/n); half = z*sqrt(p(1-p)/n + z^2/(4n^2)) / (1 + z^2/n); z = 1.96",
            "error_rank": "1-based rank, descending score, of the best key glyph whose letter equals the reference letter",
            "majority_baseline": "accuracy of always predicting the most frequent reference letter",
            "tuning_split": "k = 0..169 tuning; k = 170..339 validation",
        },
        "majority_letter": majority_letter,
        "majority_baseline": majority,
        "methods": {m: {"hits": per[m]["hits"], "n": per[m]["n"], "accuracy": per[m]["accuracy"],
                        "wilson95": per[m]["wilson95"], "errors_all": per[m]["errors_all"],
                        "error_bins_validation": per[m]["error_bins_validation"],
                        "error_bins_all": per[m]["error_bins_all"]} for m in METHODS},
    }
    path = HERE / "chart_data.json"
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main():
    style()
    per, majority_letter, majority = analyse()
    outputs = [chart_accuracy(per, majority), chart_errors(per), chart_intervals(per)]
    data_path = write_data(per, majority_letter, majority, outputs)
    print("checks passed: stored accuracies reproduced; M5 validation = 116/170; "
          "M5 validation error bins = 29/11/14; M0 all = 207/340")
    for path in outputs + [data_path]:
        print("wrote", path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
