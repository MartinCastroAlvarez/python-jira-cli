"""
Jira CLI.

Reference:
- https://jira.readthedocs.io/en/master/api.html
- https://confluence.atlassian.com/jiracoreserver073/advanced-searching-861257209.html
"""

import os
import time
import json
import begin

import colored

from jira import JIRA


def not_empty(d: dict=None) -> dict:
    """
    Returns another dictionary that does
    not have any null values.

    @param d: Any dict.
    
    @raises ValueError: If dict is invalid.

    @returns: Cleaned dict.
    """
    if not d or not isinstance(d, dict):
        raise ValueError("Invalid dict:", d)
    return {
        k: v
        for k, v in d.items()
        if v is not None
    }


class Profile(object):
    """
    Profile entity..

    Example:
    {
        "account": "account",
        "username": "username",
        "password": "password"
        "people": {
            "me": "currentUser()",
            "mc": "martin.castro"
        }
    }
    """

    USERNAME = 'username'
    PASSWORD = 'password'
    ACCOUNT = 'account'
    PEOPLE = 'people'

    def __init__(self, profile: dict=None) -> None:
        """
        Constructing profile.

        @raises ValueError: If profile is empty.
        @raises TypeError: If profile is not a valid dict.
        """
        if not profile:
            raise ValueError(profile)
        if not isinstance(profile, dict):
            raise TypeError(type(profile))
        self.__data = profile
        self.__people = None

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Profile: {}>".format(self.to_json())

    def get_credentials(self) -> tuple:
        """
        Credentials auth getter.
        """
        return (self.username, self.password)

    def get_host(self) -> str:
        """
        JIRA host getter.
        """
        return "https://{}.atlassian.net".format(self.account)

    @property
    def people(self) -> dict:
        """
        Access people book.

        @raises KeyError: If key name is not in JSON credentials.
        @raises ValueError: If key name is empty.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if self.__people is None:
            if not self.__data:
                raise AttributeError("profile")
            if self.PEOPLE not in self.__data:
                raise KeyError(self.PEOPLE)
            if not self.__data[self.PEOPLE]:
                raise ValueError(self.PEOPLE)
            if not isinstance(self.__data[self.PEOPLE], dict):
                raise TypeError(self.__data[self.PEOPLE])
            self.__people = People(self.__data[self.PEOPLE])
        return self.__people

    @property
    def username(self) -> str:
        """
        Access username.

        @raises KeyError: If key name is not in JSON credentials.
        @raises ValueError: If key name is empty.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if not self.__data:
            raise AttributeError("profile")
        if self.USERNAME not in self.__data:
            raise KeyError(self.USERNAME)
        if not self.__data[self.USERNAME]:
            raise ValueError(self.USERNAME)
        if not isinstance(self.__data[self.USERNAME], str):
            raise TypeError(self.USERNAME)
        return self.__data[self.USERNAME]

    @property
    def password(self) -> str:
        """
        Access password.

        @raises KeyError: If key name is not in JSON credentials.
        @raises ValueError: If key name is empty.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if not self.__data:
            raise AttributeError("profile")
        if self.PASSWORD not in self.__data:
            raise KeyError(self.PASSWORD)
        if not self.__data[self.PASSWORD]:
            raise ValueError(self.PASSWORD)
        if not isinstance(self.__data[self.PASSWORD], str):
            raise TypeError(self.PASSWORD)
        return self.__data[self.PASSWORD]

    @property
    def account(self) -> str:
        """
        Access account name.

        @raises KeyError: If key name is not in JSON credentials.
        @raises ValueError: If key name is empty.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if not self.__data:
            raise AttributeError("profile")
        if self.ACCOUNT not in self.__data:
            raise KeyError(self.ACCOUNT)
        if not self.__data[self.ACCOUNT]:
            raise ValueError(self.ACCOUNT)
        if not isinstance(self.__data[self.ACCOUNT], str):
            raise TypeError(self.ACCOUNT)
        return self.__data[self.ACCOUNT]


class People(object):
    """
    People entity.
    """

    ME = 'me'
    CURRENT_USER = 'currentUser()'

    def __init__(self, book: dict) -> None:
        """
        Constructing book of people.

        @raises TypeError: If dict of people is invalid.
        """
        if not isinstance(book, dict):
            raise TypeError(type(book))
        self.__book = book

    def find(self, name: str=None) -> str:
        """
        Tries to find the right person or returns the same.

        @param name: Name of the person to look for.

        @raises ValueError: If name is invalid.
        @raises TypeError: If name is not a valid string.
        @raises AttributeError: If book of people is invalid.

        @returns: Name of the user with that name.

        Usage:
        >>> p = People({...})
        >>> p.find("vb")
        "vaibhav.mathur"
        >>> p.find("an")
        "apeksha.naidu"
        >>> p.find("asdfasdf")
        "asdfasdf"
        >>> p.find("me")
        "currentUser()"
        """
        if not name or not isinstance(name, str):
            raise ValueError(name)
        if not isinstance(name, str):
            raise TypeError(type(name))
        if not isinstance(self.__book, dict):
            raise AttributeError(self.__book)
        if name.lower() == self.ME:
            return self.CURRENT_USER
        if name.lower() in self.__book:
            return self.__book[name.lower()]
        return name


class Configuration(object):
    """
    Configuration file entity.
    """

    def __init__(self, config_path: str=None) -> None:
        """
        Constructing Profile file.

        @param config_path: Configuration file name.

        @raises ValueError: If path name is empty.
        @raises TypeError: if path name is not a valid string.
        @raises RuntimeError: If config file is not a valid file.
        """
        if not config_path:
            raise ValueError("config_path")
        if not isinstance(config_path, str):
            raise TypeError("config_path")
        if not os.path.isfile(config_path):
            raise RuntimeError("File not found:", config_path)
        self.__config_path = config_path

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Configuration: {}>".format(self.__config_path)

    def get_profile(self, profile_name: str=None) -> Profile:
        """
        Public method to access profile.

        @param profile_name: Profile name.

        @raises ValueError: If name is empty.
        @raises TypeError: If name is an invalid string.
        @raises RuntimeError: If config path is not a valid file.
        @raises KeyError: If name is not found in the profiles file.
        @raises ValueError: If file is not a valid JSON file.

        @returns: Profile instance.
        """
        if not profile_name:
            raise ValueError("profile_name")
        if not isinstance(profile_name, str):
            raise TypeError("profile_name")
        if not os.path.isfile(self.__config_path):
            raise RuntimeError("File not found:", self.__config_path)
        with open(self.__config_path, "r") as file_buffer:
            data = json.loads(file_buffer.read().strip())
        if not data:
            raise RuntimeError(self.__config_path)
        if not isinstance(data, dict):
            raise RuntimeError(type(data))
        if profile_name not in data:
            raise KeyError(profile_name)
        if not data[profile_name]:
            raise RuntimeError("profile_name")
        return Profile(data[profile_name])


class Attlasian(object):
    """
    Atlassian connection entity.
    """

    def __init__(self, profile: Profile) -> None:
        """
        Constructing JIRA connector.

        @raises TypeError: If profile is invalid.
        """
        if not isinstance(profile, Profile):
            raise TypeError(type(profile))
        self.__profile = profile
        self.__jira = None

    @property
    def jira(self) -> object:
        """
        JIRA connection getter.
        """
        if not self.__jira:
            self.__jira = JIRA(self.__profile.get_host(),
                               basic_auth=self.__profile.get_credentials())
        return self.__jira


class Description(object):
    """
    Flags descriptions.
    """

    class Script(object):
        """
        Script descriptions.
        """
        PROFILE_NAME = "Config. profile name."
        CONFIG_PATH = "Config. file path."

    class Search(object):
        """
        Search action descriptions.
        """
        ASSIGNEE = "Search tickets by assignee."
        MINE = "Search tickets assigned to your."
        IS_TASK = "Search for tasks only."
        IS_BUG = "Search for bugs only."
        PROJECT = "Search tickets by project such as 'SAF'."
        ORDER = "Ordering key."
        TYPE = "Search tickets by type."
        ONGOING = "Search ongoing tickets."
        STATUS = "Search tickets by status."
        EPIC = "Search tickets by epic."
        PAGES = "Amount of pages to list."
        LIMIT = "Page size."

    class Create(object):
        """
        Create action descriptions.
        """
        ID = "Project ID"
        DESCRIPTION = "Set ticket description."
        ASSIGNEE = "Set assignee."
        PRIORITY = "Set priority."
        SUMMARY = "Set ticket summary."
        EPIC = "Set ticket epic such as 'SAF-2185'."
        TYPE = "Set ticket type used when creating a ticket."
        PROJECT = "Set project used when creating a ticket."
        COMPONENTS = "Set components."
        IS_TASK = "New ticket is a Task."
        IS_EPIC = "New ticket is an Epic."
        IS_BUG = "New ticket is a Bug."
        LABELS = "Set ticket labels."

    class Projects(object):
        """
        Projects action descriptions.
        """
        ID = "Project ID."

    class Comment(object):
        """
        Comment action descriptions.
        """
        ID = "Ticket ID."
        TEXT = "Comment text or type."
        CC = "Copy people in comment."
        UPLOAD = "Upload file to ticket."

    class Update(object):
        """
        Update action descriptions.
        """
        DESCRIPTION = "Update ticket description."
        ASSIGNEE = "Update assignee."
        PRIORITY = "Update priority."
        STATUS = "Update ticket status."
        SUMMARY = "Update ticket summary."
        EPIC = "New epic ticket such as 'SAF-2185'."
        NOTIFY = "Notify changes."
        COMPONENTS = "Update components."
        IS_COMPLETE = "Set ticket as completed."
        IN_BACKLOG = "Set ticket in Backlog."
        IN_OPEN =  "Set ticket in Open."
        IN_CODE_REVIEW = "Set ticket In Code Review."
        IN_PROGRESS = "Set ticket In Progress."
        WONT_FIX = "Set ticket in Won't Fix."
        IS_BLOCKED = "Set ticket as Blocked."
        IN_VALIDATION = "Set ticket In Validation."
        LABELS = "Update ticket labels."


class Fields(object):
    """
    Fields enum.
    """
    NAME = "name"
    EPIC = "customfield_10200"
    EPIC_NAME = "Epic Link"
    ASSIGNEE = "assignee"
    REPORTER = "reporter"
    STATUS = "status"
    PROJECT = "project"
    PRIORITY = "priority"
    PRIORITY_NAME = "name"
    LABELS = "labels"
    DESCRIPTION = "description"
    COMPONENTS = "components"
    SUMMARY = "summary"
    TYPE = "issuetype"
    SET = "set"
    ADD = "add"


class Type(object):
    """
    Issue type.
    """
    BUG = "Bug"
    TASK = "Task"
    STORY = "Story"
    EPIC = "Epic"


class Priority(object):
    """
    Ticket priority enum.
    """
    URGENT = "P0"
    HIGH = "P1"
    NORMAL = "P2"


class Status(object):
    """
    Ticket status enum.
    """
    DUPLICATE = "Duplicate"
    IN_VALIDATION = "In Validation"
    IN_CODE_REVIEW = "In Code Review"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    OPEN = "Open"
    BLOCKED = "Blocked"
    MOCKUPS = "Mockups"
    WONT_FIX = "Won't Fix"
    BY_DESIGN = "By Design"
    IN_DEVELOPMENT = "In Development"
    BACKLOG = "Backlog"
    AD_CREATIVE = "Ad Creative"

    MAP = {
        WONT_FIX: '71',
        DUPLICATE: '61',
        MOCKUPS: '221',
        IN_VALIDATION: '171',
        OPEN: '111',
        IN_PROGRESS: '21',
        COMPLETED: '151',
        IN_CODE_REVIEW: '201',
        BLOCKED: '161',
        BY_DESIGN: '81',
        IN_DEVELOPMENT: '211',
        BACKLOG: '101',
        AD_CREATIVE: '231'
    }


class Stdout(object):
    """ Screen output formatter. """

    @staticmethod
    def color(*s) -> str:
        """
        Prints a colored string to STDOUT.

        @param s: List of title strings.

        @returns: A printable string.
        """
        return "{}{}{}".format(colored.fore.DARK_OLIVE_GREEN_3B,
                               " ".join(list(s)),
                               colored.style.RESET)

    @staticmethod
    def bold(*s) -> str:
        """
        Prints a colored bold string to STDOUT.

        @param s: List of title strings.

        @returns: A printable string.
        """
        return "{}{}{}{}".format(colored.style.BOLD,
                                 colored.fore.WHITE,
                                 " ".join([
                                    str(x)
                                    for x in s
                                 ]),
                                 colored.style.RESET)

    @classmethod
    def line(cls) -> None:
        """
        Prints a line.
        """
        print(cls.color("-" * 50))

    @classmethod
    def title(cls, *t) -> None:
        """
        Prints a title for one section.

        @param t: List of title strings.

        @raises ValueError: If $t is an invalid string.

        @returns: None.
        """
        if not t or not isinstance(t, tuple):
            raise ValueError("Invalid title string.")
        cls.line()
        print(cls.bold(*[
            s.upper()
            for s in t
        ]))
        cls.line()

    @classmethod
    def table(cls, key: str=None, value: str=None):
        """
        Prints a key-value pair as a table.

        @param key: Column key name.
        @param value: Column value.

        @raises ValueError: If the key or value are invalid.

        @returns: None.
        """
        if not key or not isinstance(key, str):
            raise ValueError("Invalid key name:", key)
        if key.endswith(":"):
            raise ValueError("Key ends with ':'.", key)
        if isinstance(value, (list, dict)):
            value = json.dumps(value, sort_keys=True)
        if not isinstance(value, str):
            value = str(value)
        print("{:30.30s} {:s}".format(cls.bold(key), value))


class Default(object):
    """
    Script default values.
    """
    CONFIG_PATH = os.path.join(os.sep, "home", os.getlogin(), ".opal")
    PROFILE_NAME = "ampush"


@begin.subcommand
@begin.logging
def search(assignee: Description.Search.ASSIGNEE=None,
           mine: Description.Search.MINE=False,
           ongoing: Description.Search.ONGOING=False, 
           status: Description.Search.STATUS=None, 
           task: Description.Search.IS_TASK=False,
           bug: Description.Search.IS_BUG=False,
           project: Description.Search.PROJECT=None,
           order: Description.Search.ORDER="priority desc",
           ticket_type: Description.Search.TYPE=None,
           profile_name: Description.Script.PROFILE_NAME=Default.PROFILE_NAME,
           config_path: Description.Script.CONFIG_PATH=Default.CONFIG_PATH,
           epic: Description.Search.EPIC=None,
           pages: Description.Search.PAGES=3,
           limit: Description.Search.LIMIT=50):
    """
    JIRA tickets search.
    """

    # Initializing profile.
    config  = Configuration(config_path)
    profile = config.get_profile(profile_name)
    atlassian = Attlasian(profile)

    Stdout.title("Search")
    if int(limit) > 50:
        raise ValueError("Limit is too big:", limit)
    if int(pages) <= 0:
        raise ValueError("Amount of pages is invalid:", pages)

    # Search ticket by type.
    if task:
        ticket_type = Type.TASK
    elif bug:
        ticket_type = Type.BUG

    # Build query.
    query = {
        Fields.PROJECT: project,
        Fields.EPIC_NAME: epic,
        Fields.TYPE: ticket_type,
    }
    query = [
        "'{}'={}".format(k, v)
        for k, v in query.items()
        if v is not None
    ]

    # Determine assignee.
    if mine:
        assignee = profile.people.ME
    if assignee:
        assignee = profile.people.find(assignee)
        assignee = " OR ".join([
            '{}={}'.format(Fields.ASSIGNEE, assignee),
            '{}={}'.format(Fields.REPORTER, assignee),
        ])
        query.append("({})".format(assignee))

    # Build status.
    if ongoing:
        status = " OR ".join([
            '{}="{}"'.format(Fields.STATUS, Status.IN_VALIDATION),
            '{}="{}"'.format(Fields.STATUS, Status.IN_PROGRESS),
            '{}="{}"'.format(Fields.STATUS, Status.OPEN),
            # '{}="{}"'.format(Fields.STATUS, Status.BLOCKED),
            '{}="{}"'.format(Fields.STATUS, Status.IN_DEVELOPMENT),
        ])
        query.append("({})".format(status))

    # Search tickets.
    print(json.dumps(query, indent=4, sort_keys=True))
    Stdout.line()
    query = "{} order by {}".format(" AND ".join(query), order)
    start_at = 0
    for _ in range(int(pages)):
        ticket = None
        for ticket in atlassian.jira.search_issues(query, maxResults=limit, startAt=start_at):
            params = [
                ticket.fields.priority.name,
                ticket.fields.issuetype.name,
                ticket.key,
                ticket.fields.assignee.key,
                Stdout.bold(ticket.fields.status),
                ticket.fields.summary[:80].encode('ascii', 'ignore').decode(),
            ]
            print("{:3s} {:5.5s} {:11.11s} {:25.25s} {:32.32s} {}".format(*params))
        if not ticket:
            break
        start_at += limit
        Stdout.line()


@begin.subcommand
@begin.logging
def update(*ticket_ids,
           description: Description.Update.DESCRIPTION=None,
           assignee: Description.Update.ASSIGNEE=None,
           status: Description.Update.STATUS=None,
           summary: Description.Update.SUMMARY=None,
           priority: Description.Update.PRIORITY=None,
           epic: Description.Update.EPIC=None,
           notify: Description.Update.NOTIFY=True,
           components: Description.Update.COMPONENTS=None,
           is_complete: Description.Update.IS_COMPLETE=False,
           in_backlog: Description.Update.IN_BACKLOG=False,
           in_open: Description.Update.IN_OPEN=False,
           in_code_review: Description.Update.IN_CODE_REVIEW=False,
           in_progress: Description.Update.IN_PROGRESS=False,
           profile_name: Description.Script.PROFILE_NAME=Default.PROFILE_NAME,
           config_path: Description.Script.CONFIG_PATH=Default.CONFIG_PATH,
           wont_fix: Description.Update.WONT_FIX=False,
           is_blocked: Description.Update.IS_BLOCKED=False,
           in_validation: Description.Update.IN_VALIDATION=False,
           labels: Description.Update.LABELS=None):
    """
    JIRA tickets manager.
    """

    # Initializing profile.
    config  = Configuration(config_path)
    profile = config.get_profile(profile_name)
    atlassian = Attlasian(profile)

    for ticket_id in ticket_ids:
        Stdout.title(ticket_id)
        ticket = atlassian.jira.issue(ticket_id)

        # Detecting ticket status.
        if is_blocked:
            status = Status.BLOCKED
        elif is_complete:
            status = Status.COMPLETED
        elif in_validation:
            status = Status.IN_VALIDATION
        elif wont_fix:
            status = Status.WONT_FIX
        elif in_progress:
            status = Status.IN_PROGRESS
        elif in_backlog:
            status = Status.BACKLOG
        elif in_code_review:
            status = Status.IN_CODE_REVIEW
        elif in_open:
            status = Status.OPEN
        if status and isinstance(status, str):
            if status not in Status.MAP:
                transitions = {
                    t['name']: t['id']
                    for t in atlassian.jira.transitions(ticket)
                }
                raise ValueError("Status not supported.", transitions)
            print("New status:", status)
            atlassian.jira.transition_issue(ticket, status)

        # Reading description from file.
        if description and os.path.isfile(description):
            with open(description, 'r') as f:
                description = f.read().strip()

        # Updating ticket.
        query = not_empty({
            Fields.LABELS: [
                {
                    Fields.ADD: l
                }
                for l in labels.split(",")
            ] if labels else None,
            Fields.DESCRIPTION: description or None,
            Fields.SUMMARY: summary or None,
            Fields.ASSIGNEE: profile.people.find(assignee) if assignee else None,
            Fields.EPIC: epic or None,
            Fields.COMPONENTS: [
                {
                    Fields.ADD: {Fields.NAME: component}
                }
                for component in components.split(",")
            ] if components else None
        })
        if priority and isinstance(priority, str):
            query[Fields.PRIORITY] = {
                Fields.PRIORITY_NAME: priority,
            }
        if query:
            print(json.dumps(query, indent=4, sort_keys=True))
            ticket.update(notify=notify, **query)
        print("Updated:", ticket.key)


@begin.subcommand
@begin.logging
def comment(ticket_id: Description.Comment.ID,
            text: Description.Comment.TEXT=None,
            profile_name: Description.Script.PROFILE_NAME=Default.PROFILE_NAME,
            config_path: Description.Script.CONFIG_PATH=Default.CONFIG_PATH,
            cc: Description.Comment.CC=None,
            media: Description.Comment.UPLOAD=None):
    """
    JIRA comment manager.
    """

    # Initializing profile.
    config  = Configuration(config_path)
    profile = config.get_profile(profile_name)
    atlassian = Attlasian(profile)

    # Initialiizing.
    Stdout.title(ticket_id)

    # Getting ticket number.
    if not ticket_id or not isinstance(ticket_id, str):
        raise ValueError("Ticket ID is required.")

    # Validating text.
    if not text or not isinstance(text, str):
        raise ValueError("Invalid text")

    # Fetching text from file.
    if text and os.path.isfile(text):
        with open(text, 'r') as f:
            text = f.read().strip()
    if not text or not isinstance(text, str):
        raise ValueError("Invalid text.")

    # Adding cc.
    if cc and isinstance(cc, str):
        cc_text = (
            "[~{}]".format(profile.people.find(alias))
            for alias in cc.split(",")
        )
        text = "{}\n\ncc {}".format(text, " ".join(cc_text))

    # Commenting on ticket.
    ticket = atlassian.jira.issue(ticket_id)
    atlassian.jira.add_comment(ticket, text)
    print("Commented on:", ticket.key)


@begin.subcommand
@begin.logging
def create(description: Description.Create.DESCRIPTION=None,
           assignee: Description.Create.ASSIGNEE=None,
           summary: Description.Create.SUMMARY=None,
           epic: Description.Create.EPIC=None,
           ticket_type: Description.Create.TYPE=None,
           project: Description.Create.PROJECT=None,
           priority: Description.Create.PRIORITY=Priority.NORMAL,
           components: Description.Create.COMPONENTS=None,
           is_task: Description.Create.IS_TASK=False,
           is_epic: Description.Create.IS_EPIC=False,
           is_bug: Description.Create.IS_BUG=False,
           status: Description.Update.STATUS=None,
           is_complete: Description.Update.IS_COMPLETE=False,
           in_backlog: Description.Update.IN_BACKLOG=False,
           in_open: Description.Update.IN_OPEN=False,
           in_code_review: Description.Update.IN_CODE_REVIEW=False,
           in_progress: Description.Update.IN_PROGRESS=False,
           wont_fix: Description.Update.WONT_FIX=False,
           is_blocked: Description.Update.IS_BLOCKED=False,
           profile_name: Description.Script.PROFILE_NAME=Default.PROFILE_NAME,
           config_path: Description.Script.CONFIG_PATH=Default.CONFIG_PATH,
           in_validation: Description.Update.IN_VALIDATION=False,
           labels: Description.Create.LABELS=None):
    """
    JIRA tickets manager.
    """

    # Initializing profile.
    config  = Configuration(config_path)
    profile = config.get_profile(profile_name)
    atlassian = Attlasian(profile)

    # Validating function parameters.
    Stdout.title("New Ticket")
    if not summary or not isinstance(summary, str):
        raise ValueError("Summary is required.")
    if not description or not isinstance(description, str):
        description = summary
    if is_task:
        ticket_type = Type.TASK
    if is_bug:
        ticket_type = Type.BUG
    if is_epic:
        ticket_type = Type.EPIC
    if not ticket_type or not isinstance(ticket_type, str):
        ticket_type = Type.TASK
    if not assignee or not isinstance(assignee, str):
        raise ValueError("Assignee is required.")
    if not priority or not isinstance(priority, str):
        raise ValueError("Priority is required.")
    if epic and not project:
        project = epic.split("-")[0]
    if not project or not isinstance(project, str):
        raise ValueError("Project is required.")

    # Reading description from file.
    if description and os.path.isfile(description):
        with open(description, 'r') as f:
            description = f.read().strip()

    # Creating ticket.
    query = not_empty({
        Fields.DESCRIPTION: description,
        Fields.SUMMARY: summary,
        Fields.PROJECT: project,
        Fields.PRIORITY: {
            Fields.PRIORITY_NAME: priority,
        },
        Fields.COMPONENTS: [
            {
                Fields.ADD: {Fields.NAME: component}
            }
            for component in components.split()
        ] if components else None,
        Fields.ASSIGNEE: {
            Fields.NAME: profile.people.find(assignee),
        },
        Fields.TYPE: {
            Fields.NAME: Type.TASK
        },
        Fields.EPIC: epic or None,
    })
    print(json.dumps(query, indent=4, sort_keys=True))
    ticket = atlassian.jira.create_issue(query)
    # print(ticket.__dict__)

    # Detecting ticket status.
    status = None
    if is_blocked:
        status = Status.BLOCKED
    elif is_complete:
        status = Status.COMPLETED
    elif in_validation:
        status = Status.IN_VALIDATION
    elif wont_fix:
        status = Status.WONT_FIX
    elif in_progress:
        status = Status.IN_PROGRESS
    elif in_backlog:
        status = Status.BACKLOG
    elif in_code_review:
        status = Status.IN_CODE_REVIEW
    elif in_open:
        status = Status.OPEN

    # Updating ticket.
    if components or labels or status:
        update(ticket.key,
               status=status,
               components=components,
               labels=labels)

    print("Created:", ticket.key)


@begin.subcommand
@begin.logging
def projects(id: Description.Projects.ID=None,
             profile_name: Description.Script.PROFILE_NAME=Default.PROFILE_NAME,
             config_path: Description.Script.CONFIG_PATH=Default.CONFIG_PATH):
    """
    JIRA projects manager.
    """

    # Initializing profile.
    config  = Configuration(config_path)
    profile = config.get_profile(profile_name)
    atlassian = Attlasian(profile)

    if id:
        Stdout.title(id)
        project = atlassian.jira.project(id)
        Stdout.table("Name", project.name)
        Stdout.table("Leader", project.lead.displayName)
        print("Roles")
        roles = atlassian.jira.project_roles(project)
        for role in roles:
            Stdout.table(roles[role]['id'], role)
        print("Components:")
        for component in atlassian.jira.project_components(project):
            Stdout.table(component.id, component.name)
    else:
        Stdout.title("Projects")
        for project in atlassian.jira.projects():
            print(project, project.name)


@begin.subcommand
@begin.logging
def details(*ticket_ids,
            profile_name: Description.Script.PROFILE_NAME=Default.PROFILE_NAME,
            config_path: Description.Script.CONFIG_PATH=Default.CONFIG_PATH):
    """
    JIRA tickets details
    """

    # Initializing profile.
    config  = Configuration(config_path)
    profile = config.get_profile(profile_name)
    atlassian = Attlasian(profile)

    for ticket_id in ticket_ids:
        Stdout.title(ticket_id)
        ticket = atlassian.jira.issue(ticket_id)
        # Stdout.table("Project", ticket.fields.project.key)
        Stdout.table("Summary", ticket.fields.summary)
        Stdout.table("Priority", ticket.fields.priority.name)
        Stdout.table("Type", Stdout.color(ticket.fields.issuetype.name))
        Stdout.table("Status", ticket.fields.status)
        Stdout.table("Assignee", ticket.fields.assignee.key)
        Stdout.table("Reporter", ticket.fields.reporter.key)
        Stdout.table("Labels", json.dumps(ticket.fields.labels))
        Stdout.table("Components", json.dumps([
            c.name
            for c in ticket.fields.components
        ]))
        Stdout.table("Epic", getattr(ticket.fields, Fields.EPIC))
        Stdout.table("Created", ticket.fields.created)
        Stdout.table("Updated", ticket.fields.updated)
        Stdout.table("Resolved", ticket.fields.resolutiondate)
        Stdout.line()
        print(Stdout.color(ticket.fields.description))
        Stdout.line()
        for attachment in ticket.fields.attachment:
            print(Stdout.color(attachment.filename),
                  "|",
                  Stdout.color(attachment.author.key),
                  "|",
                  Stdout.color(attachment.created))
            print(attachment.content)
            Stdout.line()
        for comment in ticket.fields.comment.comments:
            print(Stdout.bold(comment.author.key),
                  "|",
                  Stdout.color(comment.created))
            print(comment.body)
            Stdout.line()


@begin.subcommand
@begin.logging
def close(*ticket_ids):
    """
    Alias: Close multiple JIRA tickets.
    """
    for ticket_id in ticket_ids:
        update(ticket_id, status=Status.COMPLETED)


@begin.subcommand
@begin.logging
def ongoing():
    """
    Alias: List ongoing tickets.
    """
    search(mine=True, ongoing=True)


@begin.start(lexical_order=True, short_args=True)
@begin.logging
def run():
    """
    Main task.
    This method will be called by executing this script from the CLI.
    """
