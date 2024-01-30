import argparse
import re
import sys

from transformers import pipeline

from fetch_github import extract_specific_fields, fetch_github_issues
from sentiment_analysis import predict_sentiment
from logging_setup import logging


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
    parser.add_argument("-o", "--owner", help="GitHub repository owner")
    parser.add_argument("-r", "--repo", help="GitHub repository name")
    return parser.parse_args()


def main():
    args = parse_args()

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
    issues = fetch_github_issues(owner, repo)
    results = []
    try:
        for issue in issues:
            filtered_issue = extract_specific_fields(issue)
            if args.number_choice == "0":
                model = "SamLowe/roberta-base-go_emotions"
                pipe = pipeline("text-classification", model=model)
                sentiment_results = predict_sentiment(
                    filtered_issue["text_clean"], pipe, model
                )
            elif args.number_choice == "1":
                model = "distilbert-base-uncased-finetuned-sst-2-english"
                pipe = pipeline("sentiment-analysis", model=model)
                sentiment_results = predict_sentiment(
                    filtered_issue["text_clean"], pipe, model
                )
            filtered_issue["score"] = sentiment_results["score"]
            filtered_issue["label"] = sentiment_results["label"]
            print(
                f"Title: {filtered_issue['title']} Score: {filtered_issue['score']:.4f} Label: {filtered_issue['label']}"
            )

            results.append(filtered_issue)

    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
