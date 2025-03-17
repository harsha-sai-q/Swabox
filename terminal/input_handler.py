"""
Input handler module for Swabox
"""

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory

# Session history
history = InMemoryHistory()

# Styling
style = Style.from_dict({
    'prompt': '#00aa00 bold',
})

# Default command completer
default_commands = [
    'help', 'clear', 'exit', 'history', 'echo', 'date', 
    'time', 'info', 'system', 'ai'
]

def get_user_input(prompt="swabox> ", commands=None):
    """Get user input with command completion"""
    # Create a completer with default commands plus any additional commands
    all_commands = default_commands + (commands or [])
    command_completer = WordCompleter(all_commands, ignore_case=True)
    
    # Create a session with history and completer
    session = PromptSession(
        history=history,
        completer=command_completer,
        style=style
    )
    
    # Get input
    return session.prompt(prompt)

def get_password(prompt="Password: "):
    """Get password input (masked)"""
    session = PromptSession()
    return session.prompt(prompt, is_password=True)

def get_confirmation(prompt="Are you sure? (y/n): "):
    """Get yes/no confirmation"""
    session = PromptSession()
    response = session.prompt(prompt).lower()
    return response.startswith('y')