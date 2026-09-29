# METHOD — Verify a Vaexor Séance Entry

Anyone can check that an entry's aesthetic constraints came from the cited block — not from cherry-picking after writing.

## 1. Confirm the block

Use any public Bitcoin explorer or API:

```bash
# Blockstream example
curl -sS "https://blockstream.info/api/block/<BLOCK_HASH>"
```

Or open:

- `https://blockstream.info/block/<BLOCK_HASH>`
- `https://mempool.space/block/<BLOCK_HASH>`

Check that **height**, **hash**, and **timestamp** match `seance/NNNN.md`.

Entry 0001 used:

- API: `https://blockstream.info/api/blocks/tip/height` → hash → `https://blockstream.info/api/block/<hash>`
- Height: **969169**
- Hash: `000000000000000000001913077c626d1e143fbd41054f700245dc15ba5f6153`
- Timestamp (unix): `1790692947` → `2026-09-29T14:42:27Z` (10:42:27 ET)

## 2. Recompute the seed

Rule (also encoded in `scripts/transform.py`):

1. Take the 64-character lowercase hex block hash.
2. Strip **leading** `0` characters.
3. Take the first **8** hex digits of what remains (pad with trailing zeros if somehow shorter).

```text
hash  = 000000000000000000001913077c626d1e143fbd41054f700245dc15ba5f6153
strip = 1913077c626d1e143fbd41054f700245dc15ba5f6153
seed  = 1913077c
```

Leading zeros are discarded because proof-of-work makes them common; using them would collapse every seed toward zero.

## 3. Run the transform

```bash
python3 scripts/transform.py \
  000000000000000000001913077c626d1e143fbd41054f700245dc15ba5f6153 \
  --json --glyph --svg /tmp/check-0001.svg
```

Expected for entry 0001:

| Field   | Value |
|---------|--------|
| seed    | `1913077c` |
| palette | `[1] chain-mist` (`#1a1a2e` / `#4a90d9` / `#eaeaea`) |
| mood    | `[9] patience` |
| motif   | `[1] a lighthouse over black water` |

Nibble map: index 0 → palette, 1 → mood, 2 → motif (see tables inside `scripts/transform.py`).

## 4. What verification does *not* prove

- It does **not** prove the prose is "correct" — only that palette/mood/motif match the hash.
- It does **not** imply the chain sent a message.
- It does **not** forecast price or on-chain events.

## 5. Optional: regenerate the sigil

```bash
python3 scripts/transform.py <BLOCK_HASH> --svg seance/NNNN-sigil.svg
```

Compare to the committed SVG. Geometry and colors are functions of the seed alone.
