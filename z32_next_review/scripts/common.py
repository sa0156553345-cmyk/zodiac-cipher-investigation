"""Shared paths and helpers for the z32_next_review package."""
import csv, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / 'data'
IMAGES = BASE / 'images'
RESULTS = BASE / 'results'
RESULTS.mkdir(exist_ok=True)

def read_transcription():
    labels = []
    with open(DATA / 'z32_fig1A_transcription.csv', newline='', encoding='utf-8') as f:
        for r in csv.reader(f):
            if r and r[0].isdigit():
                labels.append((int(r[0]), r[1]))
    labels.sort()
    assert [p for p, _ in labels] == list(range(1, 33))
    return [s for _, s in labels]

SYMS = read_transcription()   # SYMS[i] = symbol at input position i+1 (top 1..17, bottom 18..32)

def repeat_pairs(order):
    """order = list of input indices (0..31) in output order. Returns the output-position pairs
    that hold the same symbol. Under the homophonic rule these must carry the same letter."""
    pos = {}
    for out_pos, idx in enumerate(order):
        pos.setdefault(SYMS[idx], []).append(out_pos)
    return [tuple(v) for v in pos.values() if len(v) > 1]

def satisfied(phrase, order):
    return [phrase[a] == phrase[b] for a, b in repeat_pairs(order)]
