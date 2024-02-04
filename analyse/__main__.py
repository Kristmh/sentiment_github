import argparse
import re
import sys

from transformers import pipeline


from analyse.fetch_github import extract_specific_fields, fetch_github_issues
from analyse.sentiment_analysis import predict_sentiment
from analyse.logging_setup import logging


def is_valid_github_url(url):
    """Check if the GitHub URL is valid."""
    github_url_pattern = r"^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$"
    return re.match(github_url_pattern, url)


def format_output(filtered_issue):
    """Format output to make it more readable."""
    print(
        f"- Title: {filtered_issue['title']}\n"
        f"  Score: {filtered_issue['score']:.4f}\n"
        f"  Label: {filtered_issue['label']}\n"
        f"  URL: {filtered_issue['url']}\n"
    )


def check_args(args):
    """Check for argument dependencies."""
    if (args.owner and not args.repo) or (not args.owner and args.repo):
        raise ValueError(
            "Flag owner(-o) and repo(-r) must be used together. Ex: python main.py -o octocat -r Hello-World"
        )


def check_range(value):
    """Check if the value is within the range."""
    value = int(value)
    if value < 1 or value > 100:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid value; must be between 0 and 100"
        )
    return value


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
        "-m",
        "--model_choice",
        default="sentiment",
        choices=["sentiment", "emotion"],
        help="Choose between sentiment or emotion analysis (default: sentiment)",
    )
    parser.add_argument(
        "-e",
        "--example",
        action="store_true",
        help="Use example URL https://github.com/neovim/neovim",
    )
    parser.add_argument("-o", "--owner", help="GitHub repository owner")
    parser.add_argument("-r", "--repo", help="GitHub repository name")
    parser.add_argument(
        "-f",
        "--format",
        choices=["yes", "no"],
        default="yes",
        help="Format output to more readable text(default: yes)",
    )
    parser.add_argument(
        "-n",
        "--number",
        type=check_range,
        default=5,
        help="Number of issues to analyze (default: 5)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        check_args(args)
    except ValueError as e:
        print(str(e))
        sys.exit(1)
    # Override URL if example flag is used
    if args.example:
        args.github_url = "https://github.com/neovim/neovim"

    if not is_valid_github_url(args.github_url):
        print("Invalid GitHub repository URL.")
        sys.exit(1)

    if args.owner and args.repo:
        logging.info(f"GitHub repository owner: {args.owner}")
        owner = args.owner
        repo = args.repo
    else:
        owner, repo = args.github_url.split("/")[-2:]

    logging.info(f"GitHub repository URL: {args.github_url}")
    logging.info(f"GitHub repository owner: {owner}")
    logging.info(f"GitHub repository name: {repo}")

    # Fetch issues and exit if owner or repo is invalid
    issues = fetch_github_issues(owner, repo, args.number)

    if len(issues) == 0:
        print(f"No issues found for {owner}/{repo}.")
        sys.exit(1)

    count = 0
    print(f"Anlyzing {len(issues)} issues for {owner}/{repo}...")
    try:
        for issue in issues:
            filtered_issue = extract_specific_fields(issue)
            if args.model_choice == "emotion":
                model = "SamLowe/roberta-base-go_emotions"
                pipe = pipeline("text-classification", model=model)
                sentiment_results = predict_sentiment(
                    filtered_issue["text_clean"], pipe, model
                )
            elif args.model_choice == "sentiment":
                model = "distilbert-base-uncased-finetuned-sst-2-english"
                pipe = pipeline("sentiment-analysis", model=model)
                sentiment_results = predict_sentiment(
                    filtered_issue["text_clean"], pipe, model
                )
            filtered_issue["score"] = sentiment_results["score"]
            filtered_issue["label"] = sentiment_results["label"]
            count += 1
            print(f"Analyzed issue {count} of {args.number}...")
            if args.format == "yes":
                format_output(filtered_issue)
            else:
                print(
                    f"Title: {filtered_issue['title']} Score: {filtered_issue['score']:.4f} Label: {filtered_issue['label']}"
                )

    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
