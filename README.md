# Sentiment Analysis on GitHub issues CLI

Find sentiment of GitHub issues using machine learning.
Can choose between using 2 models.
One finds if issues are positive or negative. Model: [A version of Distilbert](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english).
The seconds finds emotions in issues like confusion, joy, nervousness, surprise. Model [Based on roberta model](https://huggingface.co/SamLowe/roberta-base-go_emotions).

![analysis](assets/analysis.gif)

## Why?

This tool can help developers understand how they write issues and how the reader perceives the language used when writing issues.
When reading issues you can get an insight into what emotion the creator of the issues used, for example if they are confused or angry.
The user do not need to have any knowledge of the GitHub API or machine learning to use this tool. Just run one command to analyse your favorite repository.

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Kristmh/sentiment_github.git
```

Cd into the project

```bash
cd sentiment_github
```

Recommended: create a virtual environment using venv (or your favorite tool):

```bash
python -m venv .venv
```

Activate virtual environment

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the package:

```bash
pip install -e .
```

## Usage

Run example:

```bash
analysis
```

Run help to see all options:

```bash
analysis --help
```

Test with a different repo:

```bash
analysis https://github.com/python/cpython
```

Example using sentiment model, owner: python, repo: cpython and format: yes

```bash
analysis -m sentiment -o python -r cpython -f yes
```

Choose between models(sentiment/emotion):

```bash
analysis -m emotion
```

Choose number of issues (between 1 and 100):

```bash
analysis -n 42
```

Select GitHub repository with owner and repo name:

```bash
analysis -o python -r cpython
```

Select between different output formats(yes/no)

```bash
analysis -f no
```

## Testing

Follow the step in the quick start section and then install the dev requirements:

```bash
pip install -r requirements_dev.txt
```

The project is setup to use pytest, mypy and black.

Run pytest with coverage:

```bash
pytest
```

Run mypy for static type checking:

```bash
mypy src
```

Run black for code formatting:

```bash
black src
```

Run everything at once with tox in new virtual environment:

```bash
tox
```

Before pushing to the repository, make sure to run locally tox and pass all the test.

When pushing the code or doing a pull request, a GitHub action workflow will trigger and run the same tests as in the tox command.
