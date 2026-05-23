"""Command-line interface for Email Account Finder."""

from __future__ import annotations

import argparse

from scanner import export_csv, export_pdf, scan_email


def print_table(results) -> None:
    """Print results in a clean terminal table."""
    website_width = max(len("Website"), *(len(result.website) for result in results))
    status_width = max(len("Status"), *(len(result.status) for result in results))

    print(f"{'Website':<{website_width}} | {'Status':<{status_width}} | Link")
    print("-" * (website_width + status_width + 32))
    for result in results:
        print(f"{result.website:<{website_width}} | {result.status:<{status_width}} | {result.link}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Legal OSINT email account finder.")
    parser.add_argument("email", help="Email address to check")
    parser.add_argument("--csv", action="store_true", help="Export results to CSV")
    parser.add_argument("--pdf", action="store_true", help="Export results to PDF")
    args = parser.parse_args()

    results = scan_email(args.email)
    print_table(results)

    if args.csv:
        print(f"\nCSV saved to: {export_csv(args.email, results)}")
    if args.pdf:
        print(f"\nPDF saved to: {export_pdf(args.email, results)}")


if __name__ == "__main__":
    main()
