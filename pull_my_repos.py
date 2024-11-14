import requests
import os
from subprocess import call

# Replace 'your_access_token' with your actual GitHub token
GITHUB_TOKEN = 'your_github_token' # Needs 'read:user' and 'repo' permissions
USERNAME = 'username'  # Replace with your GitHub username, portion of the URI

# GitHub API URL to list repositories
url = f'https://api.github.com/user/repos'
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

params = {
    'type': 'owner',  # Only repositories you own
    'per_page': 100,  # Max results per page
}

def clone_repos():
    page = 1
    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        repos = response.json()

        # Stop if no more repositories
        if not repos:
            break

        for repo in repos:
            if not repo['fork']:  # Exclude forked repositories
                clone_url = repo['ssh_url']
                print(f"Cloning {clone_url}...")
                call(['git', 'clone', clone_url])

        page += 1

clone_repos()

