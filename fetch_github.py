import json
import logging
import math
import os
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
personal_access_token = os.getenv("GITHUB_TOKEN")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_github_issues(
    owner="lazyvim",
    repo="lazyvim",
    num_issues=2,
    per_page=2,
    rate_limit=5_000,
    issues_path=Path("."),
    github_token=personal_access_token,
):
    if not issues_path.is_dir():
        issues_path.mkdir(exist_ok=True)

    batch = []
    all_issues = []
    num_pages = math.ceil(num_issues / per_page)
    base_url = "https://api.github.com/repos"
    headers = {"Authorization": f"token {github_token}"}

    for page in tqdm(range(num_pages)):
        try:
            # State=all gets both open and closed issues
            query = f"issues?page={page}&per_page={per_page}&state=all"
            issues = requests.get(f"{base_url}/{owner}/{repo}/{query}", headers=headers)
            issues.raise_for_status()
            batch.extend(issues.json())
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            break
        except json.decoder.JSONDecodeError as e:
            logging.error(f"JSON decode failed: {e}")
            break

        if len(batch) > rate_limit and len(all_issues) < num_issues:
            all_issues.extend(batch)
            batch = []  # Flush batch for next time period
            logging.info("Reached GitHub rate limit. Sleeping for one hour ...")
            time.sleep(60 * 60 + 1)

    all_issues.extend(batch)
    logging.info(f"Total number of issues fetched: {len(all_issues)}")

    return all_issues


# Extract title, url, body and if it is a pull request
# And make a new field with the cleaned text
def extract_specific_fields(issue):
    title = issue.get("title", "")
    body = issue.get("body", "")
    text_clean = clean_text(f"{title} {body}")
    # Extract only the required fields
    filtered_issue = {
        "url": issue.get("html_url"),
        "title": issue.get("title"),
        "body": issue.get("body"),
        "pull_request": issue.get("pull_request", {}).get(
            "url"
        ),  # None if not a pull request
        "text_clean": text_clean,
    }
    return filtered_issue


def clean_text(text):
    if not text:
        return text
    # Remove URLs
    text = re.sub(r"http\S+", "[URL]", text)
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)
    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    # Convert to lowercase
    text = text.lower()
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    owner = "octocat"
    repo = "Hello-World"
    issues = fetch_github_issues()
    filtered_issues = extract_specific_fields(issues[0])
    print(filtered_issues)
