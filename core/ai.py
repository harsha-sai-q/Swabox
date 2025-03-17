"""
AI integration module for Swabox
"""

import os
import json
import requests
from datetime import datetime

class AIProvider:
    """Base class for AI providers"""
    def __init__(self, config=None):
        self.config = config or {}
        
    def get_suggestion(self, context):
        """Get suggestion based on context"""
        raise NotImplementedError("Subclasses must implement get_suggestion")
        
    def process_natural_language(self, query):
        """Process natural language query"""
        raise NotImplementedError("Subclasses must implement process_natural_language")

class AnthropicProvider(AIProvider):
    """Anthropic Claude AI provider"""
    def __init__(self, config=None):
        super().__init__(config)
        self.api_key = self.config.get('api_key') or os.environ.get('ANTHROPIC_API_KEY')
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = self.config.get('model', 'claude-3-haiku-20240307')
        
    def get_suggestion(self, context):
        """Get command suggestion based on context"""
        if not self.api_key:
            return "API key not configured. Please set the ANTHROPIC_API_KEY environment variable."
            
        try:
            # Create prompt for command suggestion
            prompt = f"""
            Based on the following command history and context, suggest the next command:
            
            Command History:
            {context['command_history']}
            
            Current Directory: {context['current_directory']}
            Current Task: {context['current_task']}
            
            Suggest a command that would be helpful in this context.
            """
            
            response = self._call_api(prompt)
            return response.get('content', 'No suggestion available')
            
        except Exception as e:
            return f"Error getting suggestion: {str(e)}"
    
    def process_natural_language(self, query):
        """Process natural language query to executable command"""
        if not self.api_key:
            return "API key not configured. Please set the ANTHROPIC_API_KEY environment variable."
            
        try:
            # Create prompt for natural language processing
            prompt = f"""
            Convert the following natural language request into a terminal command:
            
            Request: {query}
            
            Provide only the executable command without any explanation.
            """
            
            response = self._call_api(prompt)
            return response.get('content', 'Could not process the request')
            
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def _call_api(self, prompt):
        """Call the Anthropic API"""
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.text}")


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""
    def __init__(self, config=None):
        super().__init__(config)
        self.api_key = self.config.get('api_key') or os.environ.get('OPENAI_API_KEY')
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = self.config.get('model', 'gpt-3.5-turbo')
        
    def get_suggestion(self, context):
        """Get command suggestion based on context"""
        if not self.api_key:
            return "API key not configured. Please set the OPENAI_API_KEY environment variable."
            
        try:
            # Create prompt for command suggestion
            prompt = f"""
            Based on the following command history and context, suggest the next command:
            
            Command History:
            {context['command_history']}
            
            Current Directory: {context['current_directory']}
            Current Task: {context['current_task']}
            
            Suggest a command that would be helpful in this context.
            """
            
            response = self._call_api(prompt)
            return response.get('choices', [{}])[0].get('message', {}).get('content', 'No suggestion available')
            
        except Exception as e:
            return f"Error getting suggestion: {str(e)}"
    
    def process_natural_language(self, query):
        """Process natural language query to executable command"""
        if not self.api_key:
            return "API key not configured. Please set the OPENAI_API_KEY environment variable."
            
        try:
            # Create prompt for natural language processing
            prompt = f"""
            Convert the following natural language request into a terminal command:
            
            Request: {query}
            
            Provide only the executable command without any explanation.
            """
            
            response = self._call_api(prompt)
            return response.get('choices', [{}])[0].get('message', {}).get('content', 'Could not process the request')
            
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def _call_api(self, prompt):
        """Call the OpenAI API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0.5
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.text}")


class AIManager:
    """Manages AI provider interactions"""
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.provider_name = self.config.get('provider', 'anthropic')
        self.provider = self._initialize_provider()
        
    def _load_config(self, config_path=None):
        """Load AI configuration"""
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
            
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f).get('ai_config', {})
            except Exception:
                pass
                
        return {
            'provider': 'anthropic',
            'model': 'claude-3-haiku-20240307',
            'api_key': None
        }
        
    def _initialize_provider(self):
        """Initialize the appropriate AI provider"""
        if self.provider_name.lower() == 'anthropic':
            return AnthropicProvider(self.config)
        elif self.provider_name.lower() == 'openai':
            return OpenAIProvider(self.config)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider_name}")
            
    def get_command_suggestion(self, context):
        """Get command suggestion based on context"""
        return self.provider.get_suggestion(context)
        
    def process_natural_language(self, query):
        """Process natural language query to executable command"""
        return self.provider.process_natural_language(query)
        
    def switch_provider(self, provider_name):
        """Switch to a different AI provider"""
        self.provider_name = provider_name
        self.config['provider'] = provider_name
        self.provider = self._initialize_provider()
        return f"Switched to {provider_name} provider"