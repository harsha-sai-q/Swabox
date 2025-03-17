"""
Swabox Core Application
"""

import os
import json
import sys
from datetime import datetime
from core.ai import AIManager

class SwaboxApp:
    """
    Main Swabox application class that manages the application state,
    history, and configuration.
    """
    
    def __init__(self):
        self.start_time = datetime.now()
        self.command_history = []
        self.config = self.load_config()
        self.ai_enabled = self.config.get('ai_enabled', False)
        self.current_directory = os.getcwd()
        self.current_task = ""
        
        # Initialize AI if enabled
        if self.ai_enabled:
            try:
                self.ai_manager = AIManager()
            except Exception as e:
                print(f"Error initializing AI: {str(e)}")
                self.ai_enabled = False
        else:
            self.ai_manager = None
        
    def load_config(self):
        """Load configuration from config file"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        default_config = {
            'ai_enabled': False,
            'ai_config': {
                'provider': 'anthropic',
                'model': 'claude-3-haiku-20240307'
            },
            'history_size': 100,
            'prompt_style': 'default',
            'plugins_enabled': True
        }
        
        # Create default config file
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
    
    def save_config(self):
        """Save current configuration to config file"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def add_to_history(self, command):
        """Add a command to history"""
        self.command_history.append({
            'command': command,
            'timestamp': datetime.now().isoformat(),
            'directory': self.current_directory
        })
        
        # Trim history if it exceeds the maximum size
        max_history = self.config.get('history_size', 100)
        if len(self.command_history) > max_history:
            self.command_history = self.command_history[-max_history:]
    
    def get_history(self):
        """Get command history"""
        return self.command_history
    
    def get_uptime(self):
        """Get application uptime"""
        return datetime.now() - self.start_time
    
    def toggle_ai(self):
        """Toggle AI features on/off"""
        self.ai_enabled = not self.ai_enabled
        self.config['ai_enabled'] = self.ai_enabled
        
        if self.ai_enabled and not self.ai_manager:
            try:
                self.ai_manager = AIManager()
            except Exception as e:
                print(f"Error initializing AI: {str(e)}")
                self.ai_enabled = False
                self.config['ai_enabled'] = False
                
        self.save_config()
        return self.ai_enabled
    
    def set_current_task(self, task):
        """Set the current task description"""
        self.current_task = task
        
    def get_ai_suggestion(self):
        """Get AI command suggestion based on context"""
        if not self.ai_enabled or not self.ai_manager:
            return "AI is not enabled. Use 'ai on' to enable AI features."
            
        context = {
            'command_history': self.command_history[-10:] if self.command_history else [],
            'current_directory': self.current_directory,
            'current_task': self.current_task
        }
        
        return self.ai_manager.get_command_suggestion(context)
    
    def process_natural_language(self, query):
        """Process natural language query to executable command"""
        if not self.ai_enabled or not self.ai_manager:
            return "AI is not enabled. Use 'ai on' to enable AI features."
            
        return self.ai_manager.process_natural_language(query)