# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Liam Kennedy
# lpkenned@uci.edu
# 81845142

import shlex

def parse_command(command_str):
    """Runs a shell stype command string into a command dictionary.
    Uses the command_str as the input.
    Will return dictionary with types and args."""
    try:
        separate = shlex.split(command_str)
        if not separate:
            raise ValueError("Empty command")
        return {"type": separate[0], "args": separate[1:]}
    except Exception:
        raise ValueError("Failed to parse command")
