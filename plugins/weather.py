"""
Weather information plugin for Swabox
"""

import requests
import json

# Define command name that will be used to invoke this plugin
command_name = "weather"

def run(args):
    """
    Get weather information for a specified location
    Usage: weather <city>
    """
    if not args:
        return "Usage: weather <city>"
        
    city = args.strip()
    
    try:
        # Using OpenWeatherMap API as an example
        # In a real implementation, you would use your API key
        # and proper error handling
        api_key = "YOUR_API_KEY"  # Replace with actual API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        # For demo purposes, return a mock response
        return f"""
Weather information for {city}:
- Temperature: 22°C
- Conditions: Partly Cloudy
- Humidity: 65%
- Wind: 12 km/h

Note: This is mock data. To get real weather data, replace the API key in the plugin.
"""
    except Exception as e:
        return f"Error getting weather information: {str(e)}"