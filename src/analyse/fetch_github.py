import re
from enum import Enum
from typing import Any, Dict, List
from datetime import datetime
import requests
from tqdm import tqdm

# Import the logging setup
import analyse.logging_setup  # noqa: F401, pylint: disable=unused-import
import logging


class fetch_status(Enum):
    SUCCESS = "success"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"


def fetch_github_issues(
    owner: str = "lazyvim",
    repo: str = "lazyvim",
    num_issues: int = 5,
    per_page: int = 100,
) -> Dict[str, Any]:
    """
    Fetches issues from a GitHub repository.

    Uses tqdm for progress indication and handles GitHub's rate limiting by
    checking the remaining requests in the response headers. If the rate limit
    is reached, it warns and returns the issues fetched so far along with a
    'rate_limited' status.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        num_issues (int): Number of issues to fetch.
        per_page (int): Number of issues to fetch per page (max 100 for GitHub API).

    Returns:
        Dict[str, Any]: A dictionary with the fetch status and list of issues.
    """

    all_issues: List[str] = []
    base_url: str = "https://api.github.com/repos"
    per_page = min(num_issues, 100)

    with tqdm(total=num_issues, desc=f"Fetching issues from {owner}/{repo}") as pbar:
        fetched_issues_count: int = 0
        page: int = 1
        while fetched_issues_count < num_issues:
            query = f"issues?page={page}&per_page={per_page}&state=all"
            response = requests.get(f"{base_url}/{owner}/{repo}/{query}")
            if response.status_code == 200:
                issues_batch = response.json()
                # Filter out pull requests
                filtered_issues = [
                    issue for issue in issues_batch if "pull_request" not in issue
                ]

                # Calculate how many new issues were actually fetched
                new_issues = min(
                    len(filtered_issues), num_issues - fetched_issues_count
                )
                all_issues.extend(filtered_issues[:new_issues])
                fetched_issues_count += new_issues
                pbar.update(new_issues)

            # If noe more requests can be made, return the issues fetched so far
            elif response.status_code == 403:
                reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                reset_datetime = datetime.fromtimestamp(reset_time).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                logging.warning(
                    f"GitHub rate limit reached. Unable to fetch more issues. You can try again after: {reset_datetime}"
                )
                return {
                    "status": fetch_status.RATE_LIMITED.value,
                    "issues": all_issues,
                }
            else:
                logging.error(f"Request failed with status code {response.status_code}")
                return {"status": fetch_status.ERROR.value, "issues": all_issues}
            page += 1

    logging.info(f"Total number of issues fetched: {len(all_issues)}")
    return {"status": fetch_status.SUCCESS.value, "issues": all_issues}


# Extract title, url, body and if it is a pull request
# And make a new field with the cleaned text
def extract_specific_fields(issue: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts the title, URL, body from a GitHub issue and generates a cleaned text field.

    The title and body are combined and cleaned using an external `clean_text` function,
    designed to remove or sanitize unnecessary characters or formatting. The resulting
    cleaned text, along with the original title, URL, and body, are returned in a new
    dictionary.
    Args:
        issue: A dictionary with keys 'title', 'html_url', and 'body', representing
               a GitHub issue's data.
    Returns:
        A dictionary with keys 'url', 'title', 'body', and 'text_clean', where
        'text_clean' is the cleaned combination of 'title' and 'body'.
    """
    title: str = issue.get("title", "")
    body: str = issue.get("body", "")
    text_clean: str = clean_text(f"{title} {body}")
    # Extract only the required fields
    filtered_issue: Dict[str, Any] = {
        "url": issue.get("html_url"),
        "title": issue.get("title"),
        "body": issue.get("body"),
        "text_clean": text_clean,
    }
    return filtered_issue


def clean_text(text: str) -> str:
    """
    Cleans the input text by removing URLs, HTML tags, special characters, numbers,
    converting to lowercase, and normalizing whitespace.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text as described above.
    """
    if not text:
        return text
    # Remove URLs
    text = re.sub(r"http\S+", "", text)
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
