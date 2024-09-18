import os
import requests
import logging

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get GitHub token and inputs from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = os.getenv("GITHUB_ORG")  # GitHub organization name from workflow input
TEAM_NAME = os.getenv("GITHUB_TEAM")  # GitHub team name from workflow input
TEAM_PERMISSION = "push"  # Options: pull, push, admin, maintain, triage

if not GITHUB_TOKEN or not ORG_NAME or not TEAM_NAME:
    logging.error("Missing environment variables for GITHUB_TOKEN, GITHUB_ORG, or GITHUB_TEAM")
    exit(1)

# GitHub authentication headers
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def rename_repo(old_name, new_name):
    url = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{old_name}"
    payload = {"name": new_name}
    
    response = requests.patch(url, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        logging.info(f"Repository renamed: {old_name} -> {new_name}")
    else:
        logging.error(f"Failed to rename {old_name}: {response.status_code} - {response.text}")

def add_team_to_repo(repo_name):
    url = f"{GITHUB_API_URL}/orgs/{ORG_NAME}/teams/{TEAM_NAME}/repos/{ORG_NAME}/{repo_name}"
    payload = {"permission": TEAM_PERMISSION}

    response = requests.put(url, json=payload, headers=HEADERS)

    if response.status_code == 204:
        logging.info(f"Team '{TEAM_NAME}' added to repo: {repo_name} with '{TEAM_PERMISSION}' permission")
    else:
        logging.error(f"Failed to add team to {repo_name}: {response.status_code} - {response.text}")

def update_repos_and_add_teams(existing_file, updated_file):
    # Read the existing repository names
    with open(existing_file, 'r') as f:
        existing_repos = [line.strip() for line in f.readlines()]

    # Read the updated repository names
    with open(updated_file, 'r') as f:
        updated_repos = [line.strip() for line in f.readlines()]

    if len(existing_repos) != len(updated_repos):
        logging.error("Mismatch between number of existing and updated repos.")
        return

    logging.info(f"Updating {len(existing_repos)} repositories and adding teams...")

    # Process renaming and team addition
    for old_repo, new_repo in zip(existing_repos, updated_repos):
        rename_repo(old_repo, new_repo)
        add_team_to_repo(new_repo)

# Example usage
existing_file = 'existing.txt'
updated_file = 'updated.txt'
update_repos_and_add_teams(existing_file, updated_file)
