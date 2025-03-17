# Swabox: AI-Integrated Terminal

Swabox is a modern terminal application enhanced with AI capabilities, providing users with intelligent assistance directly in their command-line environment.

## Features

- Basic terminal functionality with command history
- Syntax highlighting and command completion using Rich and prompt_toolkit
- Built-in commands for system information and utilities
- Plugin system for extending functionality
- Shell command execution via "!" prefix
- AI-assisted command suggestions and natural language processing (coming soon)

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
- `![command]` - Execute a shell command

## Project Structure

```
swabox/
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── swabox.py            # Main entry point
├── config.json          # Application configuration
├── terminal/            # Terminal UI components
│   ├── __init__.py
│   ├── ui.py            # UI rendering using Rich
│   └── input_handler.py # Input handling with prompt_toolkit
├── core/                # Core application logic
│   ├── __init__.py
│   ├── app.py           # Main application logic
│   ├── commands.py      # Command execution and plugin handling
│   └── ai.py            # AI integration (in development)
├── plugins/             # Plugin system
│   ├── __init__.py
│   └── weather.py       # Example weather plugin
├── services/            # Service components
│   ├── ai-service/      # JavaScript AI integration
│   ├── command-engine/  # C# command processing
│   └── plugin-system/   # Java plugin system
├── docker-compose.yml   # Docker Compose configuration
└── utils/               # Utility scripts and tools
    ├── dev/             # Development utilities
    └── setup/           # Setup scripts
```

## Plugin System

Swabox features a plugin system that allows for easy extension of functionality:

```python
# Example of loading plugins
plugins = load_plugins(plugin_folder="plugins")

# Example of executing a plugin command
execute_command("weather", plugins)
```

Plugins are loaded dynamically from the `plugins` directory. Each plugin should be a Python module with a `run()` function.

## Shell Command Execution

You can execute shell commands directly from Swabox by prefixing them with `!`:

```
Enter command: !ls -la
```

This will execute the `ls -la` command in your system shell.

## Theme and Styling

Swabox uses the Rich library for terminal styling with a custom theme:

- `info`: dim cyan - for informational messages
- `warning`: magenta - for warning messages
- `error`: bold red - for error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)