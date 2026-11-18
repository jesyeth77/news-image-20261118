# news-image-20261118 — "Sum up 18 November's world news in one image"

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)

Built for the [make.fun bounty "Sum up 18 November's world news in one image"](https://make.fun/bounty/news-image-20261118) ($250, top 50 share the prize).

A one-page newspaper-style infographic (1024×1024 PNG) summarising the real
world news of Wednesday 18 November 2026: the U.S. strike on Iran's Qeshm
Island and the Gulf escalation, the Kerch Bridge to Crimea partly
collapsing, the Ebola outbreak in DR Congo, the U.S. losing measles-free
status, and Mary Peltola's Alaska win giving Democrats 56 Senate seats —
plus three more stories in "Also today".

## How it works

- `main.py` (the entry program, pure standard library) copies the baked
  image `assets/entry.png` to `/output/entry.png` and verifies it meets the
  bounty limits (PNG, at most 1024×1024, at most 1 MiB). No network, no
  randomness — running it twice writes identical bytes.
- `render.py` is the generator that drew `assets/entry.png` from the news
  data in `data/news.json` (Pillow + the bundled DejaVu fonts). Re-run it
  to reproduce the image exactly.
- `data/news.json` holds the baked news (headlines, summaries, sources).

## The news (all real, 18 Nov 2026)

1. **U.S. strikes Iran's Qeshm Island as Tehran's drones hit Bahrain and Kuwait** — U.S. jets hit a Revolutionary Guard missile site after Iranian drones targeted a U.S. radar base in Bahrain; Tehran then fired drones at Bahrain and Kuwait. (CBS News, Al Jazeera, The Japan Times)
2. **Kerch Bridge to Crimea partly collapses after Ukrainian strikes** — a road span fell into the strait on the second day of attacks; rail service later resumed. (One Turn News, Horizon)
3. **Ebola in DR Congo more than doubles in three months** — the UN counts 11,000 cases and 5,400 deaths; three in four infected children under five die. (United Nations)
4. **U.S. loses measles-free status after 26 years** — PAHO ends the status held since 2000: 5,412 cases, 10 deaths, the worst outbreak since 1991. (PAHO, The Hill, The Guardian)
5. **Peltola wins Alaska; Democrats reach 56 Senate seats** — Mary Peltola unseats Republican Dan Sullivan, flipping the ninth seat for a 56–44 majority. (Associated Press, Reuters, CNBC)
6. Also today: Russian military plane crashes in Siberia (19 dead); magnitude 6.0 earthquake in Papua New Guinea; Category 5 Cyclone Xavier hits the Northern Cook Islands.

## Verification

- `python3 main.py` run twice: identical sha256
  `8e7ca1f4c9388783176a9d0f89b056c79ab993cb70c2d85e00d36239e74620a7`,
  1024×1024, 134,656 bytes (≤1 MiB).

## License

MIT. DejaVu fonts in `fonts/` are under the DejaVu license (free, redistributable).
