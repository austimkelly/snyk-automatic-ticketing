#create_jira_ticket.py

# While this API call will work. There's some issues.
# 1) The data pull from. Snyk to find out if there's an issue associated does not update immediatly. I'm not sure how long it taskes.
# 2) As such, the API itself does not check if an issue already exist and will yeild duplicates.
# 3) However, the vulnerabity itself in Snyk does have the ability to show multiple JIRA lins in case of duplicates.

# SNYK_TOKEN is using Jupyter style secrets. Change to fetch from env variable if you go that route.
snyk_api_token = SNYK_TOKEN
# add in the org id(s) for the Synk orgs you want to pull from
org_id = os.environ.get("ORG_ID")

# Jira Key - Typically the 2-4 letter code for the project.
jira_project_id = "YOURJIRAKEY"
# Jira Issue ID. Typically an integer.
jira_issue_type_id = "ISSUETYPEID"

def process_row(row):
    org_id = os.environ["ORG_ID"]
    project_id = row["project_id"]
    issue_id = row["issue_id"]
    url = 'https://api.snyk.io/v1/org/{}/project/{}/issue/{}/jira-issue'.format(org_id, project_id, issue_id)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token {}".format(snyk_api_token)
    }
    data = {
        "fields": {
            "project": { "key": jira_project_id},
            "issuetype": { "id": jira_issue_type_id},
            "summary": row["issue_title"],
        }
    }
    print(url)
    response = requests.post(url, headers=headers, json=data)
    print(response.json())


PRIORITY_SCORE_THRESHOLD = 750

for index, row in df.iterrows():
    if pd.notnull(row["issue_jiraIssueUrl"]):
        print(row["issue_jiraIssueUrl"])
    elif row["issue_priorityScore"] > PRIORITY_SCORE_THRESHOLD:
        process_row(row)