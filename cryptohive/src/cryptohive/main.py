"""CLI entry point for CryptoHive."""

import sys
from dotenv import load_dotenv


def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print("Usage: python -m cryptohive.main \"<query>\"")
        print("Example: python -m cryptohive.main \"Analyze BTC\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"\n{'='*60}")
    print(f"  CryptoHive")
    print(f"  Query: {query}")
    print(f"{'='*60}\n")

    from cryptohive.flow import run_analysis

    result = run_analysis(query)

    print(f"\n{'='*60}")
    print("  FINAL REPORT")
    print(f"{'='*60}")
    print(result)


if __name__ == "__main__":
    main()
