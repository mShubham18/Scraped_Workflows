import os
import requests
from urllib.parse import urljoin

GITHUB_REPO = "https://github.com/enescingoz/awesome-n8n-templates"
RAW_BASE_URL = "https://raw.githubusercontent.com/enescingoz/awesome-n8n-templates/main"  # or 'master'

LOCAL_SAVE_DIR = "Scraped_Workflows" 

def list_txt_files_from_github(repo_url):
    api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
    if api_url.endswith('/'):
        api_url = api_url[:-1]
    api_url += "/git/trees/main?recursive=1"

    res = requests.get(api_url)
    if res.status_code != 200:
        raise Exception("Failed to fetch repo structure")

    files = res.json()["tree"]
    txt_files = [f["path"] for f in files if f["path"].endswith(".txt")]
    return txt_files

def save_as_json(path, content):
    local_path = os.path.join(LOCAL_SAVE_DIR, path)
    local_json_path = os.path.splitext(local_path)[0] + ".json"
    os.makedirs(os.path.dirname(local_json_path), exist_ok=True)
    with open(local_json_path, "w", encoding='utf-8') as f:
        f.write(content)

def main():
    txt_files = list_txt_files_from_github(GITHUB_REPO)
    for txt_file in txt_files:
        raw_url = urljoin(RAW_BASE_URL + "/", txt_file)
        res = requests.get(raw_url)
        if res.status_code == 200:
            save_as_json(txt_file, res.text)
            print(f"Saved {txt_file} as JSON")
        else:
            print(f"Failed to fetch: {raw_url}")

if __name__ == "__main__":
    main()
