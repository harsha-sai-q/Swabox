# Swabox: AI-Integrated Terminal

Swabox is a modern terminal application enhanced with AI capabilities, providing users with intelligent assistance directly in their command-line environment.

## Features

- Basic terminal functionality with command history
- Syntax highlighting and command completion
- Built-in commands for system information and utilities
- (Coming soon) AI-assisted command suggestions
- (Coming soon) Natural language command processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/swabox.git
cd swabox
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run Swabox:
```bash
python swabox.py
```

## Available Commands

- `help` - Display available commands
- `clear` - Clear the screen
- `exit` - Exit Swabox
- `history` - Show command history
- `echo [text]` - Display the provided text
- `date` - Display the current date
- `time` - Display the current time
- `info` - Display information about Swabox
- `system` - Display system information

## Project Structure

```
swabox/
├── requirements.txt   # Python dependencies
├── swabox.py         # Main entry point
├── terminal/         # Terminal UI components
├── core/             # Core application logic
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.# terminal/ui.py
from rich.console import Console
from rich.theme import Theme

# Define a custom theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "error": "bold red"
})

console = Console(theme=custom_theme)

def display_message(message, style="info"):
    console.print(message, style=style)# terminal/input_handler.py
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import PathCompleter
    
    session = PromptSession(completer=PathCompleter())
    
    def get_user_input():
        return session.prompt("Enter command: ")# core/commands.py
        import importlib
        import os
        
        def load_plugins(plugin_folder="plugins"):
            plugins = {}
            for filename in os.listdir(plugin_folder):
                if filename.endswith(".py"):
                    module_name = filename[:-3]
                    module = importlib.import_module(f"{plugin_folder}.{module_name}")
                    plugins[module_name] = module
            return plugins
        
        def execute_command(command, plugins):
            if command in plugins:
                plugins[command].run()
            else:
                print(f"Command {command} not found.")# core/commands.py
                import subprocess
                
                def execute_command(command, plugins):
                    if command.startswith("!"):
                        shell_command = command[1:]
                        subprocess.run(shell_command, shell=True)
                    elif command in plugins:
                        plugins[command].run()
                    else:
                        print(f"Command {command} not found.")