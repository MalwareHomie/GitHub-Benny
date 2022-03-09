#Required
import requests
from pprint import pprint
from secret import GITHUB_TOKEN
import argparse
import os
import time
import sys
PYTHONIOENCODING="UTF-8"
import json

###Notes
### https://github.community/t/create-branch-protection-rules-at-an-organization-level/12368/5 
## https://github.community/t/create-branch-protection-rules-at-an-organization-level/12368/20

#GitHub Org Creds
USERNAME = 'MalwareHomie'
API_URL= "https://api.github.com"
API_PAYLOAD = '{"name":"xxxRepoNamexxx"}'
ORG_NAME = 'GithubSiliconValley'
# REPO_NAME = 'demo-ghas-verademo'
#TOKEN = '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'
# The repository to add this issue to
#REPO_OWNER = 'GithubSiliconValley'
# REPO_NAME = 'demo-ghas-verademo'
API_BP_ENDPOINT = "https://api.github.com/orgs/GithubSiliconValley"

#Branch Protection Properties
BRANCH_PROTECT = '{"required_status_checks":{"strict":true,"contexts":["contexts"]},"enforce_admins":true,"required_pull_request_reviews":{"dismissal_restrictions":{"users":["users"],"teams":["teams"]},"dismiss_stale_reviews":true,"require_code_owner_reviews":true,"required_approving_review_count":2},"restrictions":{"users":["users"],"teams":["teams"],"apps":["apps"]}}'

#Debugging help thanks to @Jonmagic (https://gist.github.com/jonmagic/5282384165e0f86ef105)
# Authentication for user creating repo 
headers = {
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept":"application/vnd.github.v3+json"
}

putheaders ={
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept":"application/vnd.github.luke-cage-preview+json"
}

#Parsing input from "webhook"...
parser = argparse.ArgumentParser()
parser.add_argument("--name","-n",type=str,dest="name",required=True)
parser.add_argument("--private","-p",dest="is_private",action="store_true")
parser.add_argument("--auto_init","-a",dest='auto_init',action="store_true")

args = parser.parse_args()
print(args)
repo_name = args.name
is_private = args.is_private
auto_init = args.auto_init

if is_private & auto_init:
    payload = '{"name": "' + repo_name + '", "private": true, "auto_init": "true"}'
else:
    payload = '{"name": "' + repo_name + '", "private": false, "auto_init": "true"}'
print(payload)

try:
    print(API_URL+"/orgs/"+ORG_NAME+"/"+"repos")
    print("Repo Created - Issue Generation and Protection Rule in Process...")
    reponse = requests.post(API_URL+"/orgs/"+ORG_NAME+"/"+"repos",data=payload,headers = headers)
    if(reponse.status_code==201):
        putresponse = requests.put(API_BP_ENDPOINT+"/"+repo_name+"/branches/main/protection",data=BRANCH_PROTECT,headers=putheaders)

    else:
        reponse.raise_for_status()

except requests.exceptions.RequestException as err:
    raise SystemExit(err)
#This script was inspired by @DerBla (https://gist.github.com/JeffPaine/3145490?permalink_comment_id=4008650#gistcomment-4008650)
# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
def make_github_issue(title, body=None, milestone=None, labels=None):
    # Create an issue on github.com using the given parameters
    # Url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (ORG_NAME, repo_name)
    
    # Headers are different for issues generation
    headers = {
        "Authorization": "token %s" % GITHUB_TOKEN,
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Create our issue
    data = {          'title': title,
                      'body': body,
                      'milestone': milestone,
                      'labels': labels}

    # Add the issue to our repository
    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    if response.status_code == 201:
        print ('Successfully created Issue "%s"' % title)
    else:
        print ('Could not create Issue "%s"' % title)
        print ('Response:', response.content)

#Args to pass thru
title = 'Protection Rule Applied'
body = '@MalwareHomie <br><b> The following Protections have been placed on the master branch:</b> <br>requiresApprovingReviews=true <br>requiresCodeOwnerReviews=true <br>requiredApprovingReviewCount=1<br>requiresStatusChecks=true<br>requiresStrictStatusChecks=false<br>requiresLinearHistory=true'
milestone = None
labels = ["ProtectionRule"]

make_github_issue(title, body, milestone, labels)

### Triggering borrowed sh script to apply protection rules by @cgpu (https://github.com/cgpu/add-branch-protection-rules) using GH CLI. 
#Can be too fast.
time.sleep(3)
#Required args for the sh script
cmd = './createBranchProtectionRule.sh \
github.com  \
GithubSiliconValley \
%s \
master \
requiresApprovingReviews=true \
requiresCodeOwnerReviews=true \
requiredApprovingReviewCount=1 \
requiresStatusChecks=true \
requiresStrictStatusChecks=false \
requiresLinearHistory=true' % (repo_name)

#Not best practice, but will need to research further. 
os.popen(cmd)