import os
import requests
from requests.auth import HTTPBasicAuth

#Test for QA Merge scrum-2-dev.

JIRA_URL = os.environ["JIRA_URL"].rstrip("/")
EMAIL = os.environ["JIRA_EMAIL"]
API_TOKEN = os.environ["JIRA_API_TOKEN"]

auth = HTTPBasicAuth(EMAIL, API_TOKEN)


print(API_TOKEN)


response = requests.get(
    f"{JIRA_URL}/rest/api/3/search/jql",
    params={
        "jql": (
            'project = DEMO AND '
            'duedate < now() AND '
            'statusCategory != Done'
        ),
        "maxResults": 50,
        "fields": "summary,status,assignee,duedate",
    },
    auth=auth,
    headers={"Accept": "application/json"},
    timeout=30,
)
response.raise_for_status()

for issue in response.json().get("issues", []):
    fields = issue["fields"]
    print(
        issue["key"],
        fields["summary"],
        fields["status"]["name"],
        fields.get("duedate"),
    )