# Sentiment Analysis on GitHub issues CLI

## Description

Find sentiment of GitHub issues and pull requests using machine learning.
Can choose between using 2 models.
One finds if issues are positive or negative. Model: [A version of Distilbert](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english).
The seconds finds emotions in issues like confusion, joy, nervousness, surprise. Model [Based on roberta model](https://huggingface.co/SamLowe/roberta-base-go_emotions).

## Why?

This tool can help developers understand how they write issues and how the reader perceives the language used when writing issues.
When reading issues you can get an insight into what emotion the creator of the issues used, for example if they are confused or angry.

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

## Usage

Run example:

```bash
python main.py
```

Run help to see all options:

```bash
python main.py --help
```

Test with a different repo:

```bash
python main.py https://github.com/python/cpython
```

Example using sentiment model, owner: python, repo: cpython and format: yes

```bash
python main.py -m sentiment -o python -r cpython -f yes
```

Choose between models(sentiment/emotion):

```bash
python main.py -m emotion
```

Select GitHub repository with owner and repo name:

```bash
python main.py -o python -r cpython
```

Select between different output formats(yes/no)

```bash
python main.py -f no
```
