from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
BASE_URL = "https://api.github.com"

def search_github_all_repos(keywords, language=None, is_pr=False, state="all", label=None):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Combine keywords into a single search query
    keyword_query = " OR ".join([f'"{keyword}"' for keyword in keywords])
    query = f"{keyword_query} type:{'pr' if is_pr else 'issue'} state:{state}"
    if language:
        query += f" language:{language}"
    if label:
        query += f" label:{label}"

    search_url = f"{BASE_URL}/search/issues"
    params = {"q": query}

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        raise Exception(f"GitHub API returned an error: {response.status_code}, {response.text}")


@app.route("/search_all", methods=["POST"])
def search_all():
    try:
        data = request.get_json()
        keywords = data.get("keywords", [])
        language = data.get("language")
        search_type = data.get("type", "issues").lower()
        state = data.get("state", "all").lower()
        label = data.get("label")

        if not keywords or not isinstance(keywords, list):
            return jsonify({"error": "Keywords must be a non-empty array"}), 400

        if search_type == "all":
            # Fetch both issues and pull requests
            issues = search_github_all_repos(keywords, language, is_pr=False, state=state, label=label)
            prs = search_github_all_repos(keywords, language, is_pr=True, state=state, label=label)
            results = {
                "issues": [{"title": item["title"], "url": item["html_url"]} for item in issues],
                "pull_requests": [{"title": item["title"], "url": item["html_url"]} for item in prs],
            }
        else:
            is_pr = search_type == "pulls"
            data = search_github_all_repos(keywords, language, is_pr, state, label)
            results = [{"title": item["title"], "url": item["html_url"]} for item in data]

        return jsonify({
            "success": True,
            "results": results,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
