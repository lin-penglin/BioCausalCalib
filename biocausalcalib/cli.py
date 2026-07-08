"""Command-line entry points for the BioCausalCalib harness."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from biocausalcalib.loader import JsonlValidationError, load_items


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="biocausalcalib")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate a benchmark JSONL file")
    validate_parser.add_argument("path", help="path to a benchmark JSONL file")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        try:
            items = load_items(args.path)
        except (JsonlValidationError, OSError) as exc:
            print(f"Validation failed: {exc}", file=sys.stderr)
            return 1

        noun = "item" if len(items) == 1 else "items"
        print(f"{len(items)} valid {noun} in {args.path}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
