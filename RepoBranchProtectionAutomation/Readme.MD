## Repo creation and issue generation

>>For master branch to be automatically protected upon creation.
> 
> >In this python application we have used simple arg parser to values from listener.
> 
>>As part of this automation we have used extensively GitHub API for creation of 
> repository and then add branch protection rule on top of it.
> 
> >Generate your token!> 
> >[GitHub PAT Token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)
```
GITHUB_TOKEN = "YourTokenPAT from GitHUB"
```

```
from secret import GITHUB_TOKEN
```

> > Only change will be in HTTP Header of both API call 
>> 1. For POST to create Repository
> >2. For PUT to update created repository branch protection rule.
> 
 ```
headers = {
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept":"application/vnd.github.v3+json"
}

putheaders ={
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept":"application/vnd.github.luke-cage-preview+json"
}

```
>  
> > In case of error requests library not found please install it using pip or pip3 python package manager.
> [Pip install](https://pypi.org/project/requests/)
>  
> 
> > In event of any exception you will be able to  view exact error message in command line from where you are running
> program.
 
>> __Reference Links__
>
> >[GitHub Create Repository API](https://docs.github.com/en/rest/reference/repos#create-an-organization-repository)
> 
> >[GitHub Update Branch Protection Rule API](https://docs.github.com/en/rest/reference/repos#update-branch-protection)
