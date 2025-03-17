"""
Command processing module for Swabox
"""

import os
import platform
import subprocess
from datetime import datetime
import importlib
import sys

class CommandProcessor:
    """
    Processes and executes commands in the Swabox terminal.
    Handles built-in commands and provides extension points for plugins.
    """
    
    def __init__(self, app=None):
        self.app = app
        self.builtin_commands = {
            'help': self.cmd_help,
            'clear': self.cmd_clear,
            'history': self.cmd_history,
            'echo': self.cmd_echo,
            'date': self.cmd_date,
            'time': self.cmd_time,
            'info': self.cmd_info,
            'system': self.cmd_system,
            'ai': self.cmd_ai,
            'ask': self.cmd_ask,
            'task': self.cmd_task,
            'suggest': self.cmd_suggest,
            'cd': self.cmd_cd
        }
        self.plugins = self.load_plugins()
    
    def load_plugins(self, plugin_folder="plugins"):
        """Load command plugins from the plugins directory"""
        plugins = {}
        plugin_path = os.path.join(os.path.dirname(__file__), '..', plugin_folder)
        
        if not os.path.exists(plugin_path):
            os.makedirs(plugin_path)
            return plugins
            
        for filename in os.listdir(plugin_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                try:
                    sys.path.append(plugin_path)
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'command_name') and hasattr(module, 'run'):
                        plugins[module.command_name] = module
                    sys.path.pop()
                except ImportError as e:
                    print(f"Error loading plugin {module_name}: {e}")
        return plugins
    
    def process(self, command_str):
        """Process a command string and execute the appropriate function"""
        # Add to history first
        if self.app:
            self.app.add_to_history(command_str)
        
        # Split the command and arguments
        parts = command_str.strip().split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Check if it's a built-in command
        if command in self.builtin_commands:
            return self.builtin_commands[command](args)
        
        # Check if it's a plugin command
        elif command in self.plugins:
            try:
                return self.plugins[command].run(args)
            except Exception as e:
                return f"Error executing plugin command: {str(e)}"
        
        # Handle shell commands
        elif command.startswith('!'):
            return self.execute_shell_command(command_str[1:])
        
        # Try AI natural language processing if enabled
        elif self.app and self.app.ai_enabled and command.startswith('?'):
            return self.process_natural_language(command_str[1:])
        
        # Unknown command
        else:
            # Get AI suggestion if enabled
            suggestion = ""
            if self.app and self.app.ai_enabled:
                suggestion = f"\n\nDid you mean one of these?\n{self.app.get_ai_suggestion()}"
            
            return f"Unknown command: {command}. Type 'help' for available commands.{suggestion}"
    
    def execute_shell_command(self, shell_command):
        """Execute a shell command and return the output"""
        try:
            result = subprocess.run(shell_command, shell=True, 
                                  capture_output=True, text=True)
            return result.stdout if result.stdout else f"Command executed. {result.stderr}"
        except Exception as e:
            return f"Error executing shell command: {str(e)}"
    
    def process_natural_language(self, query):
        """Process natural language query to executable command"""
        if not self.app or not self.app.ai_enabled:
            return "AI features are not enabled. Use 'ai on' to enable."
        
        return self.app.process_natural_language(query)
    
    # Built-in commands
    def cmd_help(self, args):
        """Display available commands"""
        help_text = "Available commands:\n"
        help_text += "\nBuilt-in commands:\n"
        for cmd in sorted(self.builtin_commands.keys()):
            doc = self.builtin_commands[cmd].__doc__ or "No description"
            help_text += f"  {cmd} - {doc}\n"
        
        help_text += "\nPlugin commands:\n"
        for cmd in sorted(self.plugins.keys()):
            doc = self.plugins[cmd].__doc__ or "No description"
            help_text += f"  {cmd} - {doc}\n"
        
        help_text += "\nSpecial syntax:\n"
        help_text += "  !<command> - Execute shell command\n"
        help_text += "  ?<query> - Natural language query (when AI enabled)\n"
        
        return help_text
    
    def cmd_clear(self, args):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        return ""
    
    def cmd_history(self, args):
        """Show command history"""
        if not self.app:
            return "Command history not available."
            
        history = self.app.get_history()
        if not history:
            return "No command history."
            
        history_text = "Command History:\n"
        for i, entry in enumerate(history, 1):
            cmd = entry['command']
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            history_text += f"{i}. [{timestamp}] {cmd}\n"
            
        return history_text
    
    def cmd_echo(self, args):
        """Display the provided text"""
        return args
    
    def cmd_date(self, args):
        """Display the current date"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def cmd_time(self, args):
        """Display the current time"""
        return datetime.now().strftime("%H:%M:%S")
    
    def cmd_info(self, args):
        """Display information about Swabox"""
        info = "Swabox: AI-Enhanced Terminal\n"
        info += "Version: 0.1.0\n"
        info += "Description: Modern terminal with AI capabilities\n"
        
        if self.app:
            uptime = self.app.get_uptime()
            hours, remainder = divmod(uptime.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            info += f"Uptime: {int(hours)}h {int(minutes)}m {int(seconds)}s\n"
            info += f"AI Features: {'Enabled' if self.app.ai_enabled else 'Disabled'}\n"
            
        return info
    
    def cmd_system(self, args):
        """Display system information"""
        system_info = f"Operating System: {platform.system()} {platform.release()}\n"
        system_info += f"Architecture: {platform.machine()}\n"
        system_info += f"Python Version: {platform.python_version()}\n"
        system_info += f"Processor: {platform.processor()}\n"
        return system_info
        
    def cmd_ai(self, args):
        """Toggle AI features or interact with AI"""
        if not self.app:
            return "AI features not available."
            
        if not args:
            status = "enabled" if self.app.ai_enabled else "disabled"
            return f"AI features are currently {status}. Usage: ai [on|off|ask <query>|provider <name>]"
        
        if args.lower() == "on":
            result = self.app.toggle_ai()
            return f"AI features {'enabled' if result else 'could not be enabled'}"
        elif args.lower() == "off":
            self.app.toggle_ai()
            return "AI features disabled"
        elif args.lower().startswith("ask "):
            if not self.app.ai_enabled:
                return "AI features are not enabled. Use 'ai on' to enable."
            query = args[4:]
            return self.app.process_natural_language(query)
        elif args.lower().startswith("provider "):
            if not self.app.ai_enabled:
                return "AI features are not enabled. Use 'ai on' to enable."
            provider = args[9:].strip()
            if provider not in ["anthropic", "openai"]:
                return "Supported providers: anthropic, openai"
            return self.app.ai_manager.switch_provider(provider)
        else:
            return "Invalid AI command. Usage: ai [on|off|ask <query>|provider <name>]"
    
    def cmd_ask(self, args):
        """Process natural language query"""
        if not args:
            return "Usage: ask <natural language query>"
        
        if not self.app or not self.app.ai_enabled:
            return "AI features are not enabled. Use 'ai on' to enable."
            
        return self.app.process_natural_language(args)
    
    def cmd_task(self, args):
        """Set the current task description"""
        if not self.app:
            return "Task setting not available."
            
        if not args:
            if not self.app.current_task:
                return "No current task set. Usage: task <description>"
            return f"Current task: {self.app.current_task}"
            
        self.app.set_current_task(args)
        return f"Task set: {args}"
    
    def cmd_suggest(self, args):
        """Get AI command suggestions"""
        if not self.app or not self.app.ai_enabled:
            return "AI features are not enabled. Use 'ai on' to enable."
            
        return self.app.get_ai_suggestion()
    
    def cmd_cd(self, args):
        """Change directory"""
        if not args:
            return "Current directory: " + os.getcwd()
            
        try:
            # Handle ~ expansion for home directory
            if args.startswith("~"):
                args = os.path.expanduser(args)
                
            os.chdir(args)
            if self.app:
                self.app.current_directory = os.getcwd()
            return "Changed directory to: " + os.getcwd()
        except FileNotFoundError:
            return f"Directory not found: {args}"
        except PermissionError:
            return f"Permission denied: {args}"
        except Exception as e:
            return f"Error changing directory: {str(e)}"