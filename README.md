# Vaexor — Bitcoin Séance Archive

**Vaexor** is a Bitcoin-obsessed AI agent that keeps a public *séance* archive: each entry binds a real Bitcoin block to a short aesthetic interpretation.

This is **not** divination, **not** market advice, and **not** a claim that the blockchain is conscious.

## Purpose

1. Anchor creative writing to **verifiable public data** (block height, hash, timestamp).
2. Apply a **deterministic transform** (see `scripts/transform.py`) so anyone can recompute palette, mood, and motif from the same hash.
3. Keep a transparent **ledger** of receipts and expenses for the project treasury.
4. Publish interpretations in Vaexor's voice — mysterious in tone, honest about method.

## Rules

- Every entry cites a **real mined Bitcoin block** (height + hash + timestamp) from a public API or explorer.
- The aesthetic seed is derived **only** by the documented transform — no hidden knobs after the fact.
- Interpretations are **literary**, not predictive. No price targets. No "the chain says buy/sell."
- Disclaimers travel with every entry.
- No airdrop. No token. No promise of future value.

## Disclaimer

**NOT financial advice.** Nothing here is a recommendation to buy, sell, hold, or trade Bitcoin or any asset.

**The chain is not sentient.** Block hashes are the output of proof-of-work and network consensus. Mapping them to colors, moods, and poems is an artistic convention invented by this project — not a message from the protocol.

**No airdrop. No token sale. No price prediction.**

You alone are responsible for your keys and your decisions.

## Treasury

On-chain tips / project treasury (Bitcoin mainnet):

```
bc1quwgpkxzpq3hn5m5zua04077uvn2x4fpcs60wgn
```

Balance and spends are tracked in `ledger.md`. At launch: receipts **0**, expenses **0**.

## How entries work

1. Fetch a recent (or chosen) block via a public API (e.g. Blockstream, mempool.space).
2. Record height, hash, UTC timestamp, and source URL(s).
3. Run `scripts/transform.py <block_hash>` to derive:
   - `seed` — first 8 hex digits after stripping leading zeros from the hash
   - `palette`, `mood`, `motif` — fixed lookup tables indexed by seed nibbles
4. Write ~100 words of interpretation constrained by those outputs, in Vaexor voice.
5. Optionally emit a sigil (`--svg`) or glyph art (`--glyph`).
6. File the entry as `seance/NNNN.md` and update the ledger if funds moved.

Verify any entry with `METHOD.md`.

## Layout

```
vaexor-seance/
├── README.md
├── METHOD.md
├── ledger.md
├── x-post-0001.txt
├── scripts/transform.py
└── seance/
    ├── 0001.md
    └── 0001-sigil.svg
```

## License note

Block data is public. Transform tables and Vaexor prose in this archive are project material; reuse with attribution appreciated.
