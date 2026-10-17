#!/usr/bin/env python3
"""Integrity and reported-results checks for the Zodiac cipher investigation repository.

Test rules, fixed before the first run of this file:
  1. Every file listed in manifests/SHA256SUMS.txt must exist and match its SHA-256; the list must cover every file except itself.
  2. No PDF, ZIP, __pycache__ folder or .pyc file may be present. PNG images are permitted only under assets/,
     and each must be listed with its SHA-256 in assets/chart_data.json (I3b).
  3. No .py or .sh file may contain an absolute path to the original working folders.
  4. Every backticked relative path in README.md, docs/*.md and the dossier must exist, except items that are declared
     external (publications, excluded images, placeholders, workspace-only names).
  5. Numbers stated in the documents are recomputed from the archived machine-readable files. Comparison precision is
     3 decimals unless the document states otherwise. A mismatch is reported as FAIL and is never corrected automatically.
  6. Statements that depend on sources outside the archive are reported as UNCHECKED.
  7. A pre-registration/code difference already recorded in the dossier is reported as DOCUMENTED-DISCREPANCY.
  8. Repository text files must contain no Arabic script (I8). The working notes were translated to English.

Usage (from the repository root):  python3 tests/check_archive.py
Requires: numpy.
"""
import collections
import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = []
ABS_MARKERS = ("/home" + "/claude", "/mnt" + "/user-data")


def rec(cid, status, detail=""):
    RESULTS.append((cid, status, detail))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def rel(path):
    return path.relative_to(ROOT).as_posix()


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def r3(x):
    return f"{float(x):.3f}"


def wilson(p, n, z=1.96):
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centre - half, centre + half


EXTERNAL_ABSENT = {
    "z32_independent_audit/input/2023-982.pdf", "z32_independent_audit/input/",
    "z32_repro/input/", "z32_next_review/input/", "z32_map_calibration_audit/input/",
    "z32_checkpoint/figures/", "z32_independent_audit/images/", "z32_map_calibration_audit/images/",
    "z32_next_review/images/", "z32_repro/images/", "z32_independent_audit.zip",
    "ZODIAC_CIPHER_INVESTIGATION.zip", "ZODIAC_CIPHER_INVESTIGATION_FINAL.zip",
    "z32_checkpoint/reproduce_z340_from_pdf.sh",
}

REQUIRED = [
    "README.md", "ZODIAC_CIPHER_RESEARCH_DOSSIER.md", "requirements.txt", ".gitignore",
    "docs/REPRODUCTION_GUIDE.md", "docs/SOURCES.md", "docs/ARCHIVE_CHANGES.md", "docs/RECORDS_INDEX.md",
    "docs/IMAGE_PROVENANCE.md", "docs/PROJECT_MAP.md", "docs/LICENSE_STATUS.md",
    "manifests/SHA256SUMS.txt", "manifests/FILE_INVENTORY.csv", "manifests/EXCLUSIONS.csv",
    "manifests/DUPLICATES_WITHIN_ARCHIVE.csv",
    "z32_checkpoint/scripts/match_v4.py", "z32_checkpoint/scripts/build_key.py", "z32_checkpoint/scripts/trans_fix.py",
    "z32_checkpoint/scripts/fix_order.py", "z32_checkpoint/scripts/verify_transposition.py",
    "z32_checkpoint/scripts/compare_z340.py", "z32_checkpoint/reproduce_z340_from_pdf.sh",
    "z32_checkpoint/methods/methods_experiment.py", "z32_checkpoint/methods/methods_results.json",
    "z32_checkpoint/methods/methods_top1_ids.json", "z32_checkpoint/methods/methods_scores.npz",
    "z32_checkpoint/methods/PREREG_METHODS.md", "z32_checkpoint/methods/VALIDATION_LOG.md",
    "z32_checkpoint/artifacts/key_table_glyphs.csv", "z32_checkpoint/artifacts/trans_values_rowmajor.json",
    "z32_checkpoint/artifacts/trans_values_fixed.json", "z32_checkpoint/artifacts/compare_z340_v4.json",
    "z32_checkpoint/artifacts/decrypt_result.json", "z32_checkpoint/artifacts/verdicts_first10.json",
    "z32_checkpoint/full63/full63_residuals.json", "z32_checkpoint/full63/robustness_results.json",
    "z32_checkpoint/full63/full63_keyids.json", "z32_checkpoint/FIRST10_MISMATCH_AUDIT.md",
    "z32_checkpoint/METHODS_REPORT.md",
    "z32_h4/PREREG_H4.md", "z32_h4/calibrate_h4.py", "z32_h4/calibration_h4.json",
    "z32_structure/PREREG_structure.md", "z32_structure/run_structure.py", "z32_structure/results_structure.json",
    "z32_phase5/PREREGISTRATION_phase5.md", "z32_phase5/phase5_summary.json",
    "z32_phase5_audit/audit_summary.json", "z32_phase5_audit/AUDIT_PHASE5_REPORT.md",
    "z32_phase5_audit/analysis/reproduce_models.py",
    "z32_independent_audit/data/z32_fig1A_transcription.csv", "z32_independent_audit/results/valid_orders.json",
    "z32_independent_audit/results/transposition_all_configs.csv",
    "z32_independent_audit/results/literal_phrase_test.csv", "z32_independent_audit/docs/AUDIT_REPORT.md",
    "z32_independent_audit/run_all.sh", "z32_independent_audit/requirements.txt", "logs/rerun_log.txt",
    "assets/make_charts.py", "assets/chart_data.json", "assets/m0_m5_letter_agreement.png",
    "assets/error_rank_distribution.png", "assets/wilson_confidence_intervals.png",
    "LICENSE", "LICENSING.md",
]


def integrity():
    pairs = []
    for line in (ROOT / "manifests/SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, path = line.split("  ", 1)
            pairs.append((digest, path))
    listed = {p for _, p in pairs}
    failing = [p for d, p in pairs if not (ROOT / p).is_file() or sha(ROOT / p) != d]
    rec("I1 sha256 of listed files", "PASS" if not failing else "FAIL",
        f"{len(pairs)} listed; failing: {failing[:5]}")

    everything = {rel(p) for p in ROOT.rglob("*") if p.is_file()}
    not_listed = sorted(everything - listed - {"manifests/SHA256SUMS.txt"})
    absent = sorted(listed - everything)
    rec("I2 coverage of SHA256SUMS", "PASS" if not not_listed and not absent else "FAIL",
        f"not listed: {not_listed[:5]}; listed but absent: {absent[:5]}")

    forbidden = [rel(p) for p in ROOT.rglob("*") if p.is_file()
                 and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}
                 and not (p.suffix.lower() == ".png" and rel(p).startswith("assets/"))]
    rec("I3 no images outside assets/, no PDFs or ZIPs", "PASS" if not forbidden else "FAIL", ", ".join(forbidden[:5]))
    chart_json = ROOT / "assets/chart_data.json"
    if chart_json.exists():
        listed = json.loads(chart_json.read_text(encoding="utf-8")).get("outputs", {})
        unlisted = [rel(p) for p in sorted((ROOT / "assets").glob("*.png"))
                    if p.name not in listed or sha(p) != listed[p.name]["sha256"]]
        rec("I3b assets PNGs listed in chart_data.json with matching SHA-256", "PASS" if not unlisted else "FAIL",
            ", ".join(unlisted[:5]) or f"{len(listed)} images")
    else:
        rec("I3b assets PNGs listed in chart_data.json with matching SHA-256", "FAIL", "assets/chart_data.json missing")

    caches = [rel(p) for p in ROOT.rglob("*") if "__pycache__" in p.parts or p.suffix == ".pyc"]
    rec("I4 no caches", "PASS" if not caches else "FAIL", f"{len(caches)} cache entries")

    abs_hits = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".sh"}:
            text = p.read_text(encoding="utf-8", errors="replace")
            if any(marker in text for marker in ABS_MARKERS):
                abs_hits.append(rel(p))
    rec("I5 no absolute workspace paths in code", "PASS" if not abs_hits else "FAIL", ", ".join(abs_hits[:5]))

    arabic = re.compile("[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")
    arabic_hits = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".txt", ".py", ".sh", ".json", ".csv", ".log", ".yml", ".yaml", ".cfg", ".toml"}:
            if arabic.search(p.read_text(encoding="utf-8", errors="replace")):
                arabic_hits.append(rel(p))
    rec("I8 no Arabic script in repository text files", "PASS" if not arabic_hits else "FAIL",
        ", ".join(arabic_hits[:5]) or "0 files")

    top = ("z32_", "docs/", "logs/", "manifests/", "tests/", "README", "ZODIAC_", "requirements", ".gitignore")
    unresolved = {}
    for doc in ["README.md", "ZODIAC_CIPHER_RESEARCH_DOSSIER.md"] + sorted(rel(p) for p in (ROOT / "docs").glob("*.md")):
        text = (ROOT / doc).read_text(encoding="utf-8")
        bad = []
        for ref in set(re.findall(r"`([^`\s]+)`", text)):
            if not ref.startswith(top) or "*" in ref or ref in EXTERNAL_ABSENT:
                continue
            if Path(ref).suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".zip"} or "PLACE_" in ref:
                continue
            if not (ROOT / ref.rstrip("/")).exists():
                bad.append(ref)
        if bad:
            unresolved[doc] = sorted(bad)
    rec("I6 documentation references resolve", "PASS" if not unresolved else "FAIL",
        json.dumps(unresolved, ensure_ascii=False)[:500])

    missing = [f for f in REQUIRED if not (ROOT / f).exists()]
    rec("I7 required files present", "PASS" if not missing else "FAIL", ", ".join(missing))


def reported():
    methods = load_json("z32_checkpoint/methods/methods_results.json")["results"]
    keyids = load_json("z32_checkpoint/full63/full63_keyids.json")
    vals = load_json("z32_checkpoint/artifacts/trans_values_rowmajor.json")["values"]
    pos = {v: p for p, v in enumerate(vals)}
    ref = load_json("z32_checkpoint/artifacts/compare_z340_v4.json")["ref"]
    Z = np.load(ROOT / "z32_checkpoint/methods/methods_scores.npz")

    acc = {}
    for m in ["M0", "M1", "M2", "M3", "M4", "M5"]:
        S = Z[m]
        ok = np.array([keyids[int(np.argmax(S[pos[k]]))][0] == ref[k] for k in range(340)])
        acc[m] = ok
        st = methods[m]
        same = (r3(ok[:170].mean()) == r3(st["tune"]) and r3(ok[170:].mean()) == r3(st["val"])
                and r3(ok.mean()) == r3(st["all"]))
        rec(f"C1 {m} accuracies recomputed from scores", "PASS" if same else "FAIL",
            f"tune {r3(ok[:170].mean())}/{r3(st['tune'])}, val {r3(ok[170:].mean())}/{r3(st['val'])}, "
            f"all {r3(ok.mean())}/{r3(st['all'])}")

    top1 = load_json("z32_checkpoint/methods/methods_top1_ids.json")["M5"]
    same_ids = all(top1[k] == keyids[int(np.argmax(Z["M5"][pos[k]]))] for k in range(340))
    rec("C2 M5 top-1 identities match stored list", "PASS" if same_ids else "FAIL")

    report = (ROOT / "z32_checkpoint/METHODS_REPORT.md").read_text(encoding="utf-8")
    stated = {}
    for line in report.splitlines():
        head = re.match(r"\|\s*(M[0-5])\b", line)
        ci = re.search(r"(\d\.\d{3})–(\d\.\d{3})", line)
        if head and ci:
            stated[head.group(1)] = (ci.group(1), ci.group(2))
    for m in ["M0", "M1", "M2", "M3", "M4", "M5"]:
        successes = round(methods[m]["val"] * 170)
        lo, hi = wilson(successes / 170, 170)
        calc = (r3(lo), r3(hi))
        rec(f"C3 {m} validation interval (Wilson, n=170)", "PASS" if stated.get(m) == calc else "FAIL",
            f"stated {stated.get(m)}, recomputed {calc}")

    S5, ok5 = Z["M5"], acc["M5"]
    wrong = [k for k in range(170, 340) if not ok5[k]]
    rec("C4 M5 validation mismatches", "PASS" if len(wrong) == 54 else "FAIL", f"{len(wrong)} of 170")
    margin = {}
    for k in range(170, 340):
        s = np.sort(S5[pos[k]])[::-1]
        margin[k] = float(s[0] - s[1])
    mc = np.median([margin[k] for k in range(170, 340) if ok5[k]])
    mw = np.median([margin[k] for k in wrong])
    rec("C5 median margins, M5 validation", "PASS" if (r3(mc), r3(mw)) == ("0.050", "0.022") else "FAIL",
        f"correct {r3(mc)}, wrong {r3(mw)} (stated 0.050 and 0.022)")
    bins = {"2-5": 0, "6-10": 0, ">10": 0}
    for k in wrong:
        order = np.argsort(S5[pos[k]])[::-1]
        best = min(i + 1 for i, idx in enumerate(order) if keyids[idx][0] == ref[k])
        bins["2-5" if best <= 5 else ("6-10" if best <= 10 else ">10")] += 1
    rec("C6 best reference-letter rank among M5 errors", "PASS"
        if (bins["2-5"], bins["6-10"], bins[">10"]) == (29, 11, 14) else "FAIL", str(bins))
    never = sorted(set(keyids) - set(top1))
    rec("C7 key glyphs never chosen as top-1 (M5)", "PASS" if never == ["A04", "L02", "S02", "U03"] else "FAIL",
        str(never))

    res = load_json("z32_checkpoint/full63/full63_residuals.json")
    counts = (res["agree_full"], res["agree_corrected"], len(res["residuals"]))
    rec("C8 full-340 agreement and residuals", "PASS" if counts == (207, 213, 127) else "FAIL", str(counts))
    rb = {"2-5": 0, "6-10": 0, ">10": 0}
    for r in res["residuals"]:
        b = r["rank_of_best_reference_glyph"]
        rb["2-5" if b <= 5 else ("6-10" if b <= 10 else ">10")] += 1
    rec("C9 residual rank bins (full-340)", "PASS" if (rb["2-5"], rb["6-10"], rb[">10"]) == (75, 27, 25) else "FAIL",
        str(rb))
    conf = collections.Counter((r["chosen_letter"], r["reference"]) for r in res["residuals"])
    want = {("R", "A"): 7, ("T", "R"): 6, ("D", "O"): 5, ("Y", "E"): 5}
    rec("C10 confusion counts", "PASS" if all(conf[k] == v for k, v in want.items()) else "FAIL",
        str({f"{a}->{b}": conf[(a, b)] for a, b in want}))
    rec("C11 unused glyphs in full-340 residual file", "PASS"
        if sorted(res["unused"]) == ["B02", "P02", "R04", "S02"] else "FAIL", str(res["unused"]))

    rob = load_json("z32_checkpoint/full63/robustness_results.json")
    s = rob["summary"]
    border = sum(1 for f in rob["flags"].values() if f["border"])
    close = sum(1 for f in rob["flags"].values() if f["close_neighbour"])
    got = (s["window30"]["top1_changed"], s["window42"]["top1_changed"], s["rot+4"]["top1_changed"],
           s["rot-4"]["top1_changed"], border, close)
    rec("C12 robustness counts", "PASS" if got == (24, 18, 58, 70, 5, 2) else "FAIL", str(got))

    num = [[vals[r * 17 + c] for c in range(17)] for r in range(20)]

    def decim(rr, cc, n, off):
        for k in range(n * 17):
            if k % n == rr and (2 * k) % 17 == cc:
                return k + off

    def single_row(c, off):
        return off + next(k for k in range(17) if (2 * k) % 17 == c)

    s1 = sum(num[r][c] != decim(r, c, 9, 0) for r in range(9) for c in range(17))
    s2 = sum(num[r][c] != decim(r - 9, c, 9, 153) for r in range(9, 18) for c in range(17))
    s3 = sum(num[18][c] != single_row(c, 306) for c in range(17))
    s4 = sum(num[19][c] != single_row(c, 323) for c in range(17))
    perm = sorted(vals) == list(range(340))
    rec("C13 transposition: section disagreements (1, 2, row19, row20) and permutation",
        "PASS" if (s1, s2, s3, s4) == (0, 62, 16, 15) and perm else "FAIL",
        f"{(s1, s2, s3, s4)}, permutation {perm}")
    fixed = load_json("z32_checkpoint/artifacts/trans_values_fixed.json")
    rec("C14 visual OCR corrections recorded", "PASS" if len(fixed["corrections"]) == 14 else "FAIL",
        str(len(fixed["corrections"])))

    comp = load_json("z32_checkpoint/artifacts/compare_z340_v4.json")
    dec = load_json("z32_checkpoint/artifacts/decrypt_result.json")
    rec("C15 reference length 340 (260 + 80), agreement 0.609",
        "PASS" if len(ref) == 340 and len(dec["raw"]) == 260 and r3(comp["pos_acc"]) == "0.609" else "FAIL",
        f"len(ref)={len(ref)}, block1={len(dec['raw'])}, pos_acc={r3(comp['pos_acc'])}")

    cal = load_json("z32_h4/calibration_h4.json")["results"]
    expect = {1.0: ("0.980", "0.963", "0.001"), 0.9: ("0.923", "0.797", "0.001"),
              0.8: ("0.713", "0.583", "0.001"), 0.7: ("0.500", "0.330", "0.010")}
    got_cal = {}
    for r in cal:
        key = "H0" if r["wrong_key"] else r["f_correct"]
        got_cal[key] = (r3(r["power_p001"]), r3(r["power_p0025"]), r3(r["median_p"]))
    ok = all(got_cal.get(k) == v for k, v in expect.items()) and got_cal.get("H0") == ("0.010", "0.000", "0.488")
    rec("C16 H4a calibration table", "PASS" if ok else "FAIL", str(got_cal))

    st = load_json("z32_structure/results_structure.json")
    rec("C17 structure R and K", "PASS" if (st.get("R_OBS"), st.get("K_OBS")) == (3, 29) else "FAIL",
        str((st.get("R_OBS"), st.get("K_OBS"))))
    rd = st.get("readability", {})
    by_prefix = {}
    for key in sorted(rd):
        pre = key.split("_")[0]
        by_prefix[pre] = r3(rd[key]["p"])
    want_p = {"O1": "0.788", "O2": "0.490", "O3": "0.510", "O4": "0.457"}
    rec("C18 readability p-values (O1-O4)", "PASS" if by_prefix == want_p
        else ("FAIL" if by_prefix else "UNCHECKED"), str(by_prefix))
    power = st.get("power")
    rec("C19 readability control power (2 of 20)", "PASS" if power is not None and r3(power) == "0.100"
        else "FAIL", str(power))

    audit = load_json("z32_phase5_audit/audit_summary.json")
    p5 = load_json("z32_phase5/phase5_summary.json")
    geo = (r3(audit["cand_dist_mi"]), r3(audit["cand_bearing"]),
           r3(audit["cand_geom"]["E-CCW"]["offset_deg"]), r3(audit["cand_geom"]["E-CCW"]["min_dist_mi"]))
    rec("C20 candidate geometry (distance, bearing, offset, minimum)",
        "PASS" if geo == ("13.352", "284.461", "6.348", "1.476") else "FAIL", str(geo))
    def close(stated, value):
        decimals = len(stated.split(".")[1]) if "." in stated else 0
        return abs(float(stated) - float(value)) <= 0.5 * 10 ** (-decimals) + 1e-9

    pairs = [("4.833", p5["S_lo"]), ("7.486", p5["S_hi"]), ("26.58", p5["D_min"]), ("33.69", p5["D_max"])]
    ok21 = all(close(stated, value) for stated, value in pairs)
    rec("C21 scale band and San Francisco distances (stated precision)", "PASS" if ok21 else "FAIL",
        "; ".join(f"stated {st} vs computed {float(v):.4f}" for st, v in pairs))

    vo = load_json("z32_independent_audit/results/valid_orders.json")
    n_valid = len(vo) if isinstance(vo, list) else None
    rec("C22 valid readings (34)", "PASS" if n_valid == 34 else ("FAIL" if n_valid is not None else "UNCHECKED"),
        f"type {type(vo).__name__}, length {n_valid}")
    cfg = list(csv.DictReader((ROOT / "z32_independent_audit/results/transposition_all_configs.csv")
                              .open(encoding="utf-8")))
    rec("C23 configurations (204)", "PASS" if len(cfg) == 204 else "FAIL", f"rows {len(cfg)}")
    rerun = sum(1 for line in (ROOT / "logs/rerun_log.txt").read_text(encoding="utf-8", errors="replace").splitlines()
                if "identical" in line)
    rec("C24 re-run identity checks (12)", "PASS" if rerun == 12 else "FAIL", str(rerun))

    pre = (ROOT / "z32_structure/PREREG_structure.md").read_text(encoding="utf-8")
    code = (ROOT / "z32_structure/run_structure.py").read_text(encoding="utf-8")
    pre_100k = "100000" in pre or "100 000" in pre
    code_20k = "20000" in code
    status = "DOCUMENTED-DISCREPANCY" if pre_100k and code_20k else ("PASS" if not pre_100k else "FAIL")
    rec("C25 structure simulations, pre-registration vs code", status,
        f"pre-registration states 100000: {pre_100k}; code uses 20000: {code_20k} (dossier item C17)")
    h4p = (ROOT / "z32_h4/PREREG_H4.md").read_text(encoding="utf-8")
    h4c = (ROOT / "z32_h4/calibrate_h4.py").read_text(encoding="utf-8")
    rec("C26 H4a replicates and permutations, text-level", "PASS"
        if all(t in h4p and t in h4c for t in ["300", "999"]) else "FAIL", "300 replicates and 999 permutations")
    atext = (ROOT / "z32_independent_audit/docs/AUDIT_REPORT.md").read_text(encoding="utf-8")
    rec("C27 phrase statistic 3544 and p = 0.417 (report text only)", "PASS" if "3544" in atext and "0.417" in atext
        else "FAIL", "text presence in AUDIT_REPORT.md; not recomputed")

    rec("U1 publication facts (dates, arXiv header, Foxon statements)", "UNCHECKED",
        "source PDFs are not in the archive")
    rec("U2 '44.75 to 103.11 miles' endpoint distances", "UNCHECKED", "no archived file found that contains them")
    rec("U3 literal phrase test rows (paper order satisfies 1 of 3 pairs)", "UNCHECKED",
        "header not parsed in this test; see dossier section 7")
    rec("U4 web and FBI sources", "UNCHECKED", "not stored; network disabled")


def main():
    integrity()
    reported()
    width = max(len(c) for c, _, _ in RESULTS)
    for cid, status, detail in RESULTS:
        print(f"{status:<24} {cid:<{width}}  {detail}")
    counts = collections.Counter(s for _, s, _ in RESULTS)
    print("\nSUMMARY:", dict(counts))
    return 1 if counts.get("FAIL") else 0


if __name__ == "__main__":
    sys.exit(main())
