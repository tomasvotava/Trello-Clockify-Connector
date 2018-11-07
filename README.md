# Trello-Clockify Connector
Connector for Clockify.me that feeds tasks from Trello.
As of now the connector has very limited functionality:

1. List all cards on single Trello board.
2. List all tasks in single Clockify project.
3. Non-existing Clockify tasks are created.

Optional
- Do not include Trello cards without tags (labels).
- Include tags (labels) in task name.

## Configuration
See *sample-config.json* file for directives.

**Note: The help system (-h, -trello, -clockify and -configure parameters) does not work for now.**

## Warning
*Keep your API keys and tokens as private as possible.**

## Requirements
### Python 3
Found at [oficial website](https://www.python.org/)
### python-requests
Best installed via PIP
```
pip install requests
```
or
```
python3 -m pip install requests
```