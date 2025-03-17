"""
Terminal UI module for Swabox
"""

from rich.console import Console
from rich.theme import Theme
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
import os

# Define a custom theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "error": "bold red",
    "success": "green",
    "command": "yellow",
    "highlight": "bold cyan"
})

console = Console(theme=custom_theme)

def display_message(message, style="info"):
    """Display a message with the specified style"""
    console.print(message, style=style)

def display_code(code, language="python"):
    """Display code snippet with syntax highlighting"""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)

def display_table(title, columns, data):
    """Display data in a table format"""
    table = Table(title=title)
    
    for column in columns:
        table.add_column(column)
    
    for row in data:
        table.add_row(*row)
    
    console.print(table)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')