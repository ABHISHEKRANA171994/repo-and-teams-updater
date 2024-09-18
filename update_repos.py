import pandas as pd
from github import Github
import os

# Load the CSV file
csv_file = 'mapping.csv'
df = pd.read_csv(csv_file)

# Initialize GitHub client
g = Github(os.getenv('GITHUB_TOKEN'))

# Get the organization
org_name = "your-organization-name"
org = g.get_organization(org_name)

for index, row in df.iterrows():
    old_name = row['Existing Repo Name']
    new_name = row['Updated Repo Name']
    
    # Get the repo
    try:
        repo = org.get_repo(old_name)
        print(f"Renaming repo {old_name} to {new_name}...")
        repo.edit(name=new_name)
        print(f"Repository renamed successfully from {old_name} to {new_name}.")
    except Exception as e:
        print(f"Failed to rename repo {old_name}: {e}")
