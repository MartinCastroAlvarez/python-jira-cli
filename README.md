# Opal
*JIRA CLI*

![alt text](./opal.jpg)

## Installation
```
git clone ssh://git@github.com/MartinCastroAlvarez/opal
cd opal
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```
## Configuration
Put the following content in *$HOME/.opal*
```
{
    "account": "my_company",
    "username": "###########@my_company.com",
    "password": "####",
    "project": "RXRM"
}
```

## Usage

##### Search for work in progress in this sprint
```
python3 opal.py search --mine --active --sort-by "status"
```

##### Get ticket details
```
python3 opal.py details RXRM-2864
```

##### Search for all tickets by project
```
python3 opal.py search --project RXRM
```

##### Search for all tickets assigned to you
```
python3 opal.py search --mine
```

##### Search for all tickets in validation
```
python3 opal.py search --status "in validation"
```

##### Search for all tickets assigned to user
```
python3 opal.py search --status "in progress" --assignee "martin castro"
```

##### Search for all User Stories
```
python3 opal.py search --ticket-type "story" --assignee "martin castro"
```

##### Search for all bugs
```
python3 opal.py search --ticket-type "bug" --status "in progress"
```

##### Search for all tickets in this sprint sorted by status
```
python3 opal.py search --active --sort-by "status"
```

##### Search for all tickets in this sprint sorted by assignee
```
python3 opal.py search --active --sort-by "assignee"
```

##### Search for all tickets in validation in this sprint
```
python3 opal.py search --active --status "in validation" --sort-by "assignee"
```

##### Create a new bug.
```
python3 opal.py create --priority "high" --active --status "in validation" 
```
