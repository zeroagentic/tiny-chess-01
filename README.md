# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/zeroagentic/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/zeroagentic/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in under 4 KB of Python (stdlib only, deterministic fixed-node search): alpha-beta with a transposition table, principal-variation search, null-move pruning, killers/history move ordering, quiescence with evasions, and a tapered PeSTO evaluation. Entry "MikaPrjkt 4KB Engine v32" for the make.fun tiny-chess-01 bounty.

## Run it

```sh
python3 main.py  # defines the engine; the harness imports it and calls best(position, budget)
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
