#!/usr/bin/env python3
"""
Vaexor Séance — deterministic block-hash transform.

Given a Bitcoin block hash (64 hex chars), derive:
  - seed: first 8 hex digits after stripping leading zeros
  - palette: named color triad from a fixed 16-entry table
  - mood: interpretive tone from a fixed 16-entry table
  - motif: short symbolic image from a fixed 16-entry table
  - glyph: ASCII/Unicode pattern seeded by the hash

This script does NOT predict prices, claim the chain is sentient,
or produce financial advice. It maps public block data to aesthetic
constraints for a human-written (or agent-written) interpretation.

Usage:
  python3 transform.py <block_hash> [--svg out.svg] [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

PALETTES: list[tuple[str, str, str, str]] = [
    # name, bg, accent, highlight
    ("void-ember", "#0a0a0a", "#ff3b00", "#c9a227"),  # 0
    ("chain-mist", "#1a1a2e", "#4a90d9", "#eaeaea"),  # 1
    ("hash-aurora", "#0d1b2a", "#00d4aa", "#7b2cbf"),  # 2
    ("nonce-dusk", "#1b0a0a", "#e85d04", "#ffba08"),  # 3
    ("merkle-frost", "#0b132b", "#5bc0be", "#f0f4f8"),  # 4
    ("utxo-ash", "#121212", "#8d99ae", "#ef233c"),  # 5
    ("taproot-moss", "#0f1c0f", "#52b788", "#d8f3dc"),  # 6
    ("segwit-violet", "#16001e", "#9b5de5", "#f15bb5"),  # 7
    ("halving-gold", "#1a1400", "#d4a017", "#fff3b0"),  # 8
    ("mempool-storm", "#0a0f1a", "#48cae4", "#023e8a"),  # 9
    ("oracle-ink", "#050505", "#adb5bd", "#ff6b6b"),  # a
    ("satoshi-dawn", "#1a1008", "#f4a261", "#e9c46a"),  # b
    ("lightning-arc", "#0a0014", "#c77dff", "#ffd6ff"),  # c
    ("cold-storage", "#111111", "#6c757d", "#ced4da"),  # d
    ("proof-of-time", "#001219", "#005f73", "#94d2bd"),  # e
    ("finality-crimson", "#1a0000", "#9b2226", "#ee9b00"),  # f
]

MOODS: list[str] = [
    "vigil",  # 0
    "echo",  # 1
    "ascent",  # 2
    "stillness",  # 3
    "reckoning",  # 4
    "drift",  # 5
    "resolve",  # 6
    "whisper",  # 7
    "surge",  # 8
    "patience",  # 9
    "fracture",  # a
    "bloom",  # b
    "gravity",  # c
    "mirror",  # d
    "threshold",  # e
    "return",  # f
]

MOTIFS: list[str] = [
    "a locked door with no handle",  # 0
    "a lighthouse over black water",  # 1
    "stairs ascending into fog",  # 2
    "a clock with no hands",  # 3
    "coins stacked into a tower",  # 4
    "a river that never reaches the sea",  # 5
    "roots gripping stone",  # 6
    "a sealed envelope",  # 7
    "a furnace burning quietly",  # 8
    "waves against a breakwater",  # 9
    "a cracked lens",  # a
    "a seed under frost",  # b
    "an anchor in deep current",  # c
    "two mirrors facing each other",  # d
    "a gate at dusk",  # e
    "footprints leading home",  # f
]


def derive_seed(block_hash: str) -> str:
    """First 8 hex chars after stripping leading zeros. Pad if short."""
    h = block_hash.lower().strip()
    if h.startswith("0x"):
        h = h[2:]
    if len(h) != 64 or any(c not in "0123456789abcdef" for c in h):
        raise ValueError(f"expected 64-char hex block hash, got len={len(h)}")
    significant = h.lstrip("0") or "0"
    return (significant + "00000000")[:8]


def transform(block_hash: str) -> dict[str, Any]:
    seed = derive_seed(block_hash)
    nibbles = [int(c, 16) for c in seed]
    palette_idx = nibbles[0]
    mood_idx = nibbles[1]
    motif_idx = nibbles[2]
    name, bg, accent, highlight = PALETTES[palette_idx]
    return {
        "block_hash": block_hash.lower().strip(),
        "seed": seed,
        "seed_int": int(seed, 16),
        "palette": {
            "index": palette_idx,
            "name": name,
            "bg": bg,
            "accent": accent,
            "highlight": highlight,
        },
        "mood": {"index": mood_idx, "name": MOODS[mood_idx]},
        "motif": {"index": motif_idx, "text": MOTIFS[motif_idx]},
        "nibble_map": {
            "palette": nibbles[0],
            "mood": nibbles[1],
            "motif": nibbles[2],
            "glyph_density": nibbles[3],
            "glyph_shift": nibbles[4],
            "reserved_5": nibbles[5],
            "reserved_6": nibbles[6],
            "svg_phase": nibbles[7],
        },
    }


def glyph_art(result: dict[str, Any], width: int = 32, height: int = 8) -> str:
    """Deterministic text art from seed nibbles."""
    seed = result["seed"]
    density = result["nibble_map"]["glyph_density"]
    shift = result["nibble_map"]["glyph_shift"]
    chars = " ·░▒▓█✦✧◈◉"
    # Expand seed to a PRNG-like stream via simple LCG on seed_int
    state = result["seed_int"]
    lines: list[str] = []
    threshold = density  # 0-15; higher → denser
    for y in range(height):
        row: list[str] = []
        for x in range(width):
            state = (state * 1103515245 + 12345 + shift) & 0x7FFFFFFF
            v = (state >> 16) & 0xFF
            # mix in position
            v = (v + x * 3 + y * 7 + int(seed[y % 8], 16)) & 0xFF
            level = v % 16
            if level > threshold + 4:
                ch = chars[min(9, 5 + (level % 5))]
            elif level > threshold:
                ch = chars[1 + (level % 4)]
            else:
                ch = chars[0]
            row.append(ch)
        lines.append("".join(row))
    header = f"seed:{seed} mood:{result['mood']['name']} palette:{result['palette']['name']}"
    return header + "\n" + "\n".join(lines)


def render_svg(result: dict[str, Any], size: int = 256) -> str:
    """Minimal SVG sigil from seed."""
    p = result["palette"]
    seed = result["seed"]
    phase = result["nibble_map"]["svg_phase"]
    # Circles and lines positioned from seed nibbles
    cx = size // 2
    cy = size // 2
    r_outer = 90 + phase * 2
    r_inner = 30 + result["nibble_map"]["glyph_density"] * 2
    # 8 radial ticks from seed chars
    ticks = ""
    import math

    for i, c in enumerate(seed):
        angle = (i / 8.0) * 2 * math.pi + (phase / 16.0) * (math.pi / 4)
        x1 = cx + int(r_inner * math.cos(angle))
        y1 = cy + int(r_inner * math.sin(angle))
        x2 = cx + int(r_outer * math.cos(angle))
        y2 = cy + int(r_outer * math.sin(angle))
        stroke = p["accent"] if int(c, 16) % 2 == 0 else p["highlight"]
        ticks += (
            f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="2"/>\n'
        )
    # Hexagon points from mood index
    hex_pts = []
    for i in range(6):
        angle = (i / 6.0) * 2 * math.pi - math.pi / 2
        hx = cx + int((r_outer - 20) * math.cos(angle))
        hy = cy + int((r_outer - 20) * math.sin(angle))
        hex_pts.append(f"{hx},{hy}")
    hex_str = " ".join(hex_pts)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <title>Vaexor Séance Sigil — seed {seed}</title>
  <desc>Deterministic glyph from Bitcoin block hash seed. Not financial advice.</desc>
  <rect width="100%" height="100%" fill="{p["bg"]}"/>
  <polygon points="{hex_str}" fill="none" stroke="{p["highlight"]}" stroke-width="1.5" opacity="0.7"/>
  <circle cx="{cx}" cy="{cy}" r="{r_outer}" fill="none" stroke="{p["accent"]}" stroke-width="2"/>
  <circle cx="{cx}" cy="{cy}" r="{r_inner}" fill="{p["accent"]}" opacity="0.35"/>
{ticks}  <text x="{cx}" y="{size - 16}" text-anchor="middle" fill="{p["highlight"]}"
        font-family="monospace" font-size="11">{seed}</text>
</svg>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Vaexor séance hash transform")
    parser.add_argument("block_hash", help="64-char Bitcoin block hash (hex)")
    parser.add_argument("--svg", metavar="PATH", help="write SVG sigil to PATH")
    parser.add_argument("--glyph", action="store_true", help="print text glyph art")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    try:
        result = transform(args.block_hash)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.svg:
        svg = render_svg(result)
        with open(args.svg, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {args.svg}", file=sys.stderr)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"seed:     {result['seed']}")
        print(f"seed_int: {result['seed_int']}")
        print(
            f"palette:  [{result['palette']['index']}] {result['palette']['name']} "
            f"({result['palette']['bg']} / {result['palette']['accent']} / {result['palette']['highlight']})"
        )
        print(f"mood:     [{result['mood']['index']}] {result['mood']['name']}")
        print(f"motif:    [{result['motif']['index']}] {result['motif']['text']}")
        if args.glyph:
            print()
            print(glyph_art(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
