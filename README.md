# GitHub Search API

This project is a Flask-based web application that allows users to search for GitHub issues and pull requests based on keywords, programming language, state, and labels.

## Features

- Search for GitHub issues and pull requests using keywords.
- Filter results by programming language, state, and labels.
- Fetch both issues and pull requests or specify the type of search.

## Requirements

- Python 3.6+
- Flask
- Requests

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/brebribre/github-issue-crawler.git
    cd github-search-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set your GitHub token in the `main.py` file:
    ```python
    GITHUB_TOKEN = "your_github_token"
    ```

## Usage

1. Run the Flask application:
    ```sh
    python main.py
    ```

2. Send a POST request to the `/search_all` endpoint with the following JSON payload:
    ```json
    {
        "keywords": ["keyword1", "keyword2"],
        "language": "python",
        "type": "all",  // or "issues" or "pulls"
        "state": "open",  // or "closed" or "all"
        "label": "bug"
    }
    ```

3. Example using `curl`:
    ```sh
    curl -X POST http://127.0.0.1:5000/search_all -H "Content-Type: application/json" -d '{
        "keywords": ["foldable", "folding phone"],
        "language": "Kotlin",
        "type": "all",
        "state": "open",
        "label": "bug"
    }'
    ```

## Endpoints

- **POST /search_all**: Search for GitHub issues and pull requests based on the provided criteria.
