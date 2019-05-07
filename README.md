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
    "my_company": {
        "account": "my_company",
        "username": "###########@my_company.com",
        "password": "####",
        "people": {
            "me": "currentUser()",
            "mc": "martin.castro"
        }
    }
}
```

## Usage

#### Search JIRA tickets by epic.
```
python3 opal.py search --epic PY-1111 --limit 5
```
Returns:
```
--------------------------------------------------
SEARCH
--------------------------------------------------
["'Epic Link'=PY-1111"]
--------------------------------------------------
P0  PY-1111   xxxxx.xxxxxxxx       Done              Lorem Ipsum Dolor
P0  PY-1111   xxxxx.xxxxxxxx       Done              Lorem Ipsum Dolor
P0  PY-1111   xxxxx.xxxxxxxx       Done              Lorem Ipsum Dolor
P0  PY-1111   xxxxx.xxxxxxxx       Done              Lorem Ipsum Dolor
P0  PY-1111   xxxxx.xxxxxxxx       Done              Lorem Ipsum Dolor
P0  PY-1111   xxxxx.xxxxxxxx       Done              Lorem Ipsum Dolor
P0  PY-1111   xxxxx.xxxxxxxx       Done              Lorem Ipsum Dolor
P0  PY-1111   xxxxx.xxxxxxxx       Done              Lorem Ipsum Dolor
```

#### Assign a ticket to MK.
```
python3 opal.py comment PY-1111 --text "Can you please review it?"
python3 opal.py update PY-1111 --assignee MK --in-validation
```

#### Get ticket details
```
python3 opal.py details PY-1111
```
Returns:
```
--------------------------------------------------
PY-1111
--------------------------------------------------
Summary      Lorem Ipsum Dolor
Priority     P0
Type         Bug
Status       Done
Assignee     xxxx.xxxxx
Reporter     xxxx.xxxxx
Labels       ["xxxx", "xxxx"]
Components   []
Epic         PY-1111
Created      2019-01-29T03:45:57.762-0800
Updated      2019-02-07T22:14:41.488-0800
Resolved     2019-02-07T22:14:41.482-0800
--------------------------------------------------
Issue 1 : Shipping pixels bug.

{code:java}
Uncaught TypeError: Cannot read property 'focus' of null
    at zr._fillInAddress (address-autocomplete.component.js:137)
    at Cd.A (js?key=####&libraries=places:173)
    at Object._.S.trigger (js?key=#####&libraries=places:170)
    at Gd (js?key=#####&libraries=places:69)
    at Gd (js?key=#####&libraries=places:69)
    at J2._.T.set (js?key=######&libraries=places:173)
    at J2.lg (js?key=#####&libraries=places:71)
    at b (places_impl.js:26)
    at places_impl.js:17
    at cn.e [as m] (places_impl.js:4)
{code}

cc: [~xxxxxx.xxxxx] [~xxxx.xxxxxxx]
--------------------------------------------------
Billing First and last name.mp4 | xxxx.xxxx| 2019-01-29T01:59:47.328-0800
https://my_company.atlassian.net/secure/attachment/1111111111/11111.png
--------------------------------------------------
V4.mp4 | xxxxx.xxxxx | 2019-01-29T02:00:04.051-0800
https://my_company.atlassian.net/secure/attachment/1111111111/11111.mp4
```

### Create a new bug and assign it to MC.
```
opal.py create --task --epic PY-11111 --summary "Lorem Ipsum Dolor" --assignee MC \
 --components "xxxxx" --labels "xxxxx,xxxxx,xxxxx,xxxx" \
 --description /tmp/async.txt --project PY 
```
Returns:
```
--------------------------------------------------
New Ticket
--------------------------------------------------
Created: PY-1111
```

### Mark ticket as completed:
```
python3 opal.py update PY-1111 --is-complete
```
Returns:
```
--------------------------------------------------
PY-1111
--------------------------------------------------
New status: Completed
Updated: PY-1111
```

### Add a comment from a TXT file.
```
python3 opal.py comment PY-1111 --text ./saf-1111.txt 
```
Response:
```
--------------------------------------------------
PY-1111
--------------------------------------------------
Commented on: PY-1111
```

### Create a new ticket.
```
python3 opal.py create --assignee MC --components xxxxx --description "Lorem Ipsum Dolor" --is-task --labels xxxx,xxxxx,Q22019 --summary "Lorem Ipsum Dolor" --project "PY" --in-progress
```
Returns:
```
--------------------------------------------------
NEW TICKET
--------------------------------------------------
{
    "assignee": {
        "name": "martin.castro"
    },
    "components": [
        {
            "add": {
                "name": "xxxxx"
            }
        }
    ],
    "description": "Lorem Ipsum Dolor",
    "issuetype": {
        "name": "Task"
    },
    "project": "PY",
    "summary": "Lorem Ipsum Dolor"
}
--------------------------------------------------
PY-1111
--------------------------------------------------
{
    "components": [
        {
            "add": {
                "name": "11111"
            }
        }
    ],
    "labels": [
        {
            "add": "xxxxx"
        },
        {
            "add": "Q22019"
        }
    ]
}
Updated: PY-1111
Created: PY-1111
```

### Search ongoing tickets assigned to you.
```
python3 opal.py search --mine --ongoing
```
Returns:
```
--------------------------------------------------
SEARCH
--------------------------------------------------
[
    "(assignee=currentUser() OR reporter=currentUser())",
    "(status=\"In Validation\" OR status=\"In Progress\" OR status=\"Open\" OR status=\"Blocked\" OR status=\"In Development\")"
]
--------------------------------------------------
P2  Task  PY-1111 martin.castro             In Progress    Lorem Ipsum Dolor
P2  Task  PY-1111 martin.castro             Blocked        Lorem Ipsum Dolor
P2  Task  PY-1111 martin.castro             In Progress    Lorem Ipsum Dolor
P2  Task  PY-1111 martin.castro             Blocked        Lorem Ipsum Dolor
P2  Task  PY-1111 martin.castro             In Progress    Lorem Ipsum Dolor
P2  Task  PY-1111 martin.castro             Blocked        Lorem Ipsum Dolor
--------------------------------------------------
```
You can also list ongoing tickets using this alias:
```
python3 opal.py ongoing
```

### Close JIRA Ticket.
```
python3 opal.py close PY-1111
```

#### Comment and tag people.
```
python3 opal.py comment PY-1111 --text "Can you please review it?" --cc MK,VB,GG
```
