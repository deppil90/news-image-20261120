# One Day in the World — Friday, 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/deppil90/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/deppil90/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page summing up the world news of Friday, 20 November 2026,
built for the [make.fun](https://make.fun) bounty
`news-image-20261120`.

## The image

`entry.png` (1024×1024, under 1 MiB) leads with the first-ever trilateral
summit of Donald Trump, Xi Jinping and Vladimir Putin in Shenzhen, and covers
the ICJ's ruling that Myanmar committed genocide against the Rohingya, Trump
putting any Iran decision off to 2027, Houthi strikes on Riyadh and a tanker
hit by a mine near the Strait of Hormuz, Cyclone Akvan bearing down on
Odisha, NASA confirming Voyager 1 has reached a light-day from Earth, and
Anthropic's record $81.3bn IPO — plus COP31 closing in Antalya, the Kyiv
missile strikes and the Genoa drone shutdown.

Every headline was checked against live reporting for 20 November 2026
(Reuters, BBC, The Hindu, Space, Marketscreener).

## How it works

- `draw.py` draws the front page with Pillow (session use only).
- `main.py` (Python 3.13, standard library only) copies the finished
  `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. No network, no clock —
  two runs write identical bytes.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=p2frk8rs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
