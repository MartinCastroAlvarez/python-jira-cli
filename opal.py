#/usr/bin/python3
"""
Jira CLI.

Reference:
- https://jira.readthedocs.io/en/master/api.html
- https://jira.readthedocs.io/en/master/examples.html
- https://confluence.atlassian.com/jiracoreserver073/advanced-searching-861257209.html
- https://confluence.atlassian.com/jiracoreserver073/advanced-searching-functions-reference-861257222.html
"""

import os
import time
import json
import begin

import colored

from jira import JIRA

# Loading configuration file.
CONFIG_PATH: str = os.path.join(os.sep, "home", os.getlogin(), ".opal")
if not os.path.isfile(CONFIG_PATH):
    raise OSError("Missing config file:", CONFIG_PATH)
with open(CONFIG_PATH) as file_handler:
    config: dict = json.load(file_handler)
if not config.get('account'):
    raise AttributeError('Missing "account":', CONFIG_PATH)
if not config.get('username'):
    raise AttributeError('Missing "username":', CONFIG_PATH)
if not config.get('api_token'):
    raise AttributeError('Missing "api_token":', CONFIG_PATH)

HOST: str = f'https://{config["account"]}.atlassian.net'
jira: JIRA = JIRA(HOST, basic_auth=(config['username'], config['api_token']))


class Format:
    """ Screen output formatter. """

    @staticmethod
    def color(*strings) -> str:
        """ Prints a colored string to STDOUT. """
        return "{}{}{}".format(
            colored.fore.DARK_OLIVE_GREEN_3B,
            " ".join([
                str(string)
                for string in strings
            ]),
            colored.style.RESET
        )

    @staticmethod
    def bold(*strings) -> str:
        """ Prints a colored bold string to STDOUT. """
        return "{}{}{}{}".format(
            colored.style.BOLD,
            # colored.fore.WHITE,
            colored.fore.DARK_OLIVE_GREEN_3B,
            " ".join([
                str(string)
                for string in strings
            ]),
            colored.style.RESET
        )


class Stdout:
    """ Screen output printer. """

    @staticmethod
    def dumps(data: dict) -> None:
        """ Dumps object to string. """
        if not isinstance(data, (dict, list)):
            raise TypeError(type(data))
        print(json.dumps(data, indent=4, sort_keys=True))

    @classmethod
    def line(cls) -> None:
        """
        Prints a line.
        """
        print(Format.color("-" * 50))

    @classmethod
    def title(cls, *strings) -> None:
        """ Prints the title of one section. """
        cls.line()
        print(Format.bold(" ".join([
            str(string).upper()
            for string in strings
        ])))
        cls.line()

    @classmethod
    def text(cls, *strings) -> None:
        """ Prints the text of one section. """
        print(" ".join([
            str(string)
            for string in strings
        ]))

    @classmethod
    def section(cls, title: str) -> None:
        """ Prints the title of a section. """
        if not isinstance(title, str):
            raise TypeError(type(title))
        if not title:
            raise ValueError(title)
        print(Format.bold(title))

    @classmethod
    def table(cls, key: str, value: str) -> None:
        """ Prints a key-value pair as a table. """
        if not isinstance(key, str):
            raise TypeError(type(key))
        if not key:
            raise ValueError(key)
        if isinstance(value, (list, dict)):
            value: str = json.dumps(value, sort_keys=True)
        if not isinstance(value, str):
            raise TypeError(type(value))
        print("{:30.30s} {:s}".format(Format.bold(key), value))


@begin.subcommand
@begin.logging
def search(assignee: 'Search by assignee' = '',
           mine: 'Search for tickets assigned to you' = False,
           active: 'Search in Active Sprint' = False,
           status: 'Search by status' = '',
           project: 'Search by project ' = '',
           sort_by: 'Sort key' = "priority desc",
           ticket_type: 'Search by type' = '',
           pages: 'Amount of pages' = 1,
           limit: 'Search limit.' = 50):
    """ JIRA tickets search.  """
    Stdout.title("Search")
    # Validating pagination.
    if int(limit) > 50:
        raise ValueError("Limit is too big:", limit)
    if int(pages) <= 0:
        raise ValueError("Amount of pages is invalid:", pages)
    # Build query.
    query: dict = {
        'project': project or config['project'],
        'status': status,
        'type': ticket_type,
    }
    query: list = [
        "'{}'='{}'".format(k, v)
        for k, v in query.items()
        if v
    ]
    # Determine assignee.
    if mine:
        query.append("assignee=currentUser()")
    elif assignee:
        query.append("assignee='{}'".format(assignee))
    # Search by sprint.
    if active:
        query.append('sprint IN openSprints()')
    # Search tickets.
    Stdout.dumps(query)
    Stdout.line()
    query: dict = "{} order by {}".format(" AND ".join(query), sort_by)
    for start_at in range(int(pages)):
        ticket: jira.resources.Issue = None
        for ticket in jira.search_issues(query,
                                         maxResults=limit,
                                         startAt=start_at * limit):
            print("{:10.10s} {:10.10s} {:15.15s} {:10.10s} {:20.20s} {}".format(*[
                ticket.key,
                ticket.fields.issuetype.name,
                ticket.fields.status.name,
                ticket.fields.priority.name,
                ticket.fields.assignee.displayName if ticket.fields.assignee else '',
                ticket.fields.summary[:80].encode('ascii', 'ignore').decode(),
            ]))
        if ticket is None:
            break
        Stdout.line()


@begin.subcommand
@begin.logging
def update(*ticket_ids,
           description: 'Ticket Description' = '',
           assignee: 'Ticket assignee' = '',
           status: 'Ticket status' = '',
           summary: 'Ticket summary' = '',
           priority: 'Ticket priority' = '',
           epic: 'Ticket Epic' = '',
           components: 'Ticket components' = '',
           labels: 'Ticket labels' = ''):
    """ JIRA tickets manager. """
    raise NotImplementedError()
    """
    for ticket_id in ticket_ids:
        Stdout.title(ticket_id)
        ticket = jira.issue(ticket_id)
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
                    for t in jira.transitions(ticket)
                }
                raise ValueError("Status not supported.", transitions)
            print("New status:", status)
            jira.transition_issue(ticket, status)
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
            Fields.ASSIGNEE: People.find(assignee) if assignee else None,
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
        print("Updated:", ticket.key)
    """


@begin.subcommand
@begin.logging
def comment(ticket_id: 'Ticket ID' = '',
            text: 'Comment text' = '',
            cc: 'Tag people' = '',
            media: 'Attach file' = ''):
    """ JIRA comment manager. """
    Stdout.title(ticket_id)
    if not ticket_id:
        raise ValueError("Ticket ID is required.")
    if not text:
        raise ValueError("Invalid text")
    if os.path.isfile(text):
        with open(text, 'r') as file_handler:
            text: str = file_handler.read().strip()
        if not text:
            raise ValueError("Invalid text file.")
    if person and isinstance(person, str):
        cc_text: str = ' '.join([
            "[~{}]".format(person)
            for alias in person.split(",")
        ])
        text: str = f"{text}\n\ncc {cc_text}"
    ticket: jira.resources.Issue = jira.issue(ticket_id)
    jira.add_comment(ticket, text)
    print("Commented on:", ticket.key)


@begin.subcommand
@begin.logging
def create(description: 'Ticket Description' = '',
           assignee: 'Ticket assignee' = '',
           status: 'Ticket status' = '',
           summary: 'Ticket summary' = '',
           priority: 'Ticket priority' = '',
           components: 'Ticket components' = '',
           labels: 'Ticket labels' = ''):
    """ JIRA tickets manager. """
    # Validating function parameters.
    """
    Stdout.title("New Ticket")
    if not summary or not isinstance(summary, str):
        raise ValueError("Summary is required.")
    if not description or not isinstance(description, str):
        description = summary
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
        'description': description,
        'summary': summary,
        'project': project,
        'priority': {
            'name': priority,
        },
        'components': [
            {
                'add': {'name': component}
            }
            for component in components.split()
        ] if components else None,
        'assignee': {
            'name': assignee,
        },
        'type': {
            'name': ticket_type,
        },
    })
    print(json.dumps(query, indent=4, sort_keys=True))
    ticket = jira.create_issue(query)
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
    """


@begin.subcommand
@begin.logging
def projects(id: 'Project ID' = ''):
    """ JIRA projects manager.  """
    raise NotImplementedError()
    """
    if id:
        Stdout.title(id)
        project = jira.project(id)
        Stdout.table("Name", project.name)
        Stdout.table("Leader", project.lead.displayName)
        print("Roles")
        roles = jira.project_roles(project)
        for role in roles:
            Stdout.table(roles[role]['id'], role)
        print("Components:")
        for component in jira.project_components(project):
            Stdout.table(component.id, component.name)
    else:
        Stdout.title("Projects")
        for project in jira.projects():
            print(project, project.name)
    """


@begin.subcommand
@begin.logging
def details(ticket_id: str):
    """ JIRA tickets details """
    Stdout.title(ticket_id)
    if not ticket_id:
        raise ValueError("Ticket ID is required.")
    ticket: jira.resources.Issue = jira.issue(ticket_id)
    Stdout.table("Summary", ticket.fields.summary)
    Stdout.table("URL", f'{HOST}/browse/{ticket.key}')
    # Stdout.table("Project", ticket.fields.project.key)
    Stdout.table("Type", Format.color(ticket.fields.issuetype.name))
    Stdout.table("Priority", ticket.fields.priority.name)
    Stdout.table("Status", ticket.fields.status.statusCategory.key)
    Stdout.table("Assignee", ticket.fields.assignee.displayName if ticket.fields.assignee else '')
    Stdout.table("Reporter", ticket.fields.reporter.displayName if ticket.fields.reporter else '')
    Stdout.table("Creator", ticket.fields.creator.displayName if ticket.fields.creator else '')
    Stdout.table("Labels", ', '.join(ticket.fields.labels))
    Stdout.table("Components", ', '.join([
        component.name
        for components in ticket.fields.components
    ]))
    Stdout.table("Created", ticket.fields.created)
    Stdout.table("Updated", ticket.fields.updated)
    Stdout.table("Resolved", ticket.fields.resolutiondate if ticket.fields.resolutiondate else '')
    Stdout.section("Description")
    print(ticket.fields.description)
    Stdout.line()
    for attachment in ticket.fields.attachment:
        print(Format.color(attachment.filename),
              "|",
              Format.color(attachment.author.displayName),
              "|",
              Format.color(attachment.created))
        print(attachment.content)
        Stdout.line()
    for comment in ticket.fields.comment.comments:
        print(Format.bold(comment.id),
              "|",
              Format.color(comment.author.displayName),
              "|",
              Format.color(comment.created))
        print(comment.body)
        Stdout.line()


@begin.subcommand
@begin.logging
def close(*ticket_ids):
    """ Alias: Close one or many multiple JIRA tickets. """
    raise NotImplementedError()
    """
    for ticket_id in ticket_ids:
        update(ticket_id, status=Status.COMPLETED)
    """


@begin.subcommand
@begin.logging
def ongoing():
    """ Alias: List ongoing tickets. """
    raise NotImplementedError()
    """
    search(mine=True, ongoing=True)
    """


@begin.start(lexical_order=True, short_args=True)
@begin.logging
def run():
    """
    Main task.
    This method will be called by executing this script from the CLI.
    """
