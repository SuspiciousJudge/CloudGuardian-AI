from __future__ import annotations

import argparse
import json

from app.edge_demo import edge_store


def main() -> None:
    parser = argparse.ArgumentParser(description="CloudGuardian Edge local demo utilities")
    parser.add_argument("command", choices=["seed", "reset-demo", "benchmark"])
    parser.add_argument("--runs", type=int, default=12)
    args = parser.parse_args()

    if args.command in {"seed", "reset-demo"}:
        result = edge_store.reset()
    else:
        result = edge_store.benchmark(args.runs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
