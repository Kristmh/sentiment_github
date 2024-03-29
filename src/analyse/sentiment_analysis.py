# Import the logging setup
import analyse.logging_setup  # noqa: F401, pylint: disable=unused-import
import logging

from transformers import AutoTokenizer


def predict_sentiment(issue: str, pipe, model):
    tokenizer = AutoTokenizer.from_pretrained(model)

    # Get the maximum length the model can handle
    max_length = tokenizer.model_max_length

    # Tokenize and truncate the text
    tokens = tokenizer.encode(
        issue,
        add_special_tokens=True,
        truncation=True,
        max_length=max_length,
    )

    # Convert the tokens back to text string
    truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)

    # Pass the truncated text to the pipeline
    sentiment = pipe(truncated_text)

    sentiment = {"label": sentiment[0]["label"].lower(), "score": sentiment[0]["score"]}
    logging.info(sentiment)
    return sentiment


if __name__ == "__main__":
    from transformers import pipeline
    from analyse.fetch_github import extract_specific_fields, fetch_github_issues

    data = fetch_github_issues("microsoft", "vscode")
    filtered_issue = extract_specific_fields(data["issues"][0])
    model = "SamLowe/roberta-base-go_emotions"
    pipe = pipeline("text-classification", model=model)
    sentiment_results = predict_sentiment(filtered_issue["text_clean"], pipe, model)
    print(sentiment_results)
