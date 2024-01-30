import argparse
import re
import sys


def is_valid_github_url(url):
    github_url_pattern = r"^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$"
    return re.match(github_url_pattern, url)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sentiment Analysis on GitHub repositories."
    )
    parser.add_argument(
        "github_url",
        nargs="?",
        default="https://github.com/neovim/neovim",
        help="GitHub repository URL (default: https://github.com/neovim/neovim)",
    )
    parser.add_argument(
        "-n",
        "--number_choice",
        default="0",
        choices=["0", "1"],
        help="Choose between 0 or 1 (default: 0)",
    )
    parser.add_argument(
        "-e",
        "--example",
        action="store_true",
        help="Use example URL https://github.com/neovim/neovim",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Override URL if example flag is used
    if args.example:
        args.github_url = "https://github.com/neovim/neovim"

    if not is_valid_github_url(args.github_url):
        print("Invalid GitHub repository URL.")
        sys.exit(1)
    print(f"GitHub repository URL: {args.github_url}")
    if args.number_choice == "0":
        print("You chose 0.")
    elif args.number_choice == "1":
        print("You chose 1.")


if __name__ == "__main__":
    main()
