import requests
import time
import json
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
import argparse
import logging
from configparser import ConfigParser
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weather_alerts.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("weather_alert_system")

class WeatherAlertSystem:
    """Weather Alert System that fetches data and generates alerts based on weather conditions."""
    
    def __init__(self, config_file='config.ini'):
        """Initialize the weather alert system with configuration."""
        self.config = self._load_config(config_file)
        self.api_key = self.config.get('api', 'key', fallback=os.environ.get('WEATHER_API_KEY'))
        self.base_url = self.config.get('api', 'base_url', fallback='https://api.openweathermap.org/data/2.5')
        self.units = self.config.get('preferences', 'units', fallback='imperial')
        self.locations = json.loads(self.config.get('locations', 'cities', fallback='["New York", "Los Angeles", "Chicago"]'))
        self.alert_thresholds = {
            'temp_high': float(self.config.get('alerts', 'temp_high', fallback=95)),
            'temp_low': float(self.config.get('alerts', 'temp_low', fallback=32)),
            'wind_speed': float(self.config.get('alerts', 'wind_speed', fallback=20)),
            'rain_probability': float(self.config.get('alerts', 'rain_probability', fallback=70)),
        }
        self.email_config = {
            'enabled': self.config.getboolean('email', 'enabled', fallback=False),
            'sender': self.config.get('email', 'sender', fallback=''),
            'recipients': json.loads(self.config.get('email', 'recipients', fallback='[]')),
            'smtp_server': self.config.get('email', 'smtp_server', fallback='smtp.gmail.com'),
            'smtp_port': self.config.getint('email', 'smtp_port', fallback=587),
            'username': self.config.get('email', 'username', fallback=''),
            'password': self.config.get('email', 'password', fallback='')
        }
        
        if not self.api_key:
            logger.error("API key not found. Please set it in config.ini or as WEATHER_API_KEY environment variable.")
            raise ValueError("API key is required")
            
    def _load_config(self, config_file):
        """Load configuration from INI file or create default if not exists."""
        config = ConfigParser()
        
        if not os.path.exists(config_file):
            logger.info(f"Config file {config_file} not found. Creating with default settings.")
            config['api'] = {
                'key': '',
                'base_url': 'https://api.openweathermap.org/data/2.5'
            }
            config['preferences'] = {
                'units': 'imperial',
                'check_interval': '3600'
            }
            config['locations'] = {
                'cities': '["New York", "Los Angeles", "Chicago"]'
            }
            config['alerts'] = {
                'temp_high': '95',
                'temp_low': '32',
                'wind_speed': '20',
                'rain_probability': '70'
            }
            config['email'] = {
                'enabled': 'false',
                'sender': 'your_email@gmail.com',
                'recipients': '["recipient1@example.com", "recipient2@example.com"]',
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': '587',
                'username': 'your_email@gmail.com',
                'password': 'your_app_password'
            }
            
            with open(config_file, 'w') as f:
                config.write(f)
                
        config.read(config_file)
        return config

    def get_current_weather(self, location):
        """Fetch current weather data for a location."""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': self.units
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data for {location}: {e}")
            return None

    def get_forecast(self, location):
        """Fetch 5-day forecast for a location."""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': self.units
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching forecast data for {location}: {e}")
            return None

    def generate_alerts(self, weather_data):
        """Generate alerts based on weather conditions."""
        if not weather_data:
            return []
        
        alerts = []
        temp_unit = "°F" if self.units == 'imperial' else "°C"
        speed_unit = "mph" if self.units == 'imperial' else "m/s"
        
        # Current temperature alerts
        temp = weather_data.get('main', {}).get('temp')
        if temp is not None:
            if temp > self.alert_thresholds['temp_high']:
                alerts.append({
                    'type': 'severe',
                    'title': 'Extreme Heat Warning',
                    'message': f"Temperature is {temp}{temp_unit}, which exceeds the high temperature threshold of {self.alert_thresholds['temp_high']}{temp_unit}."
                })
            elif temp < self.alert_thresholds['temp_low']:
                alerts.append({
                    'type': 'severe',
                    'title': 'Freeze Warning',
                    'message': f"Temperature is {temp}{temp_unit}, which is below the low temperature threshold of {self.alert_thresholds['temp_low']}{temp_unit}."
                })
        
        # Wind speed alerts
        wind_speed = weather_data.get('wind', {}).get('speed')
        if wind_speed is not None and wind_speed > self.alert_thresholds['wind_speed']:
            alerts.append({
                'type': 'moderate',
                'title': 'Wind Advisory',
                'message': f"Wind speed is {wind_speed}{speed_unit}, which exceeds the threshold of {self.alert_thresholds['wind_speed']}{speed_unit}."
            })
        
        # Weather condition alerts
        weather_conditions = weather_data.get('weather', [{}])
        if weather_conditions:
            main_condition = weather_conditions[0].get('main')
            description = weather_conditions[0].get('description')
            
            if main_condition == 'Thunderstorm':
                alerts.append({
                    'type': 'severe',
                    'title': 'Thunderstorm Warning',
                    'message': f"Thunderstorms detected: {description}. Take necessary precautions."
                })
            elif main_condition == 'Rain' and weather_data.get('rain', {}).get('1h', 0) > 10:
                alerts.append({
                    'type': 'moderate',
                    'title': 'Heavy Rain Alert',
                    'message': f"Heavy rainfall detected: {description}. Be aware of potential flooding."
                })
        
        return alerts

    def format_weather_display(self, weather_data, location):
        """Format weather data for display."""
        if not weather_data:
            return f"No weather data available for {location}"
        
        try:
            temp_unit = "°F" if self.units == 'imperial' else "°C"
            speed_unit = "mph" if self.units == 'imperial' else "m/s"
            
            # Extract data
            temp = weather_data.get('main', {}).get('temp')
            feels_like = weather_data.get('main', {}).get('feels_like')
            humidity = weather_data.get('main', {}).get('humidity')
            wind_speed = weather_data.get('wind', {}).get('speed')
            description = weather_data.get('weather', [{}])[0].get('description', 'Unknown')
            
            # Format timestamp
            timestamp = datetime.fromtimestamp(weather_data.get('dt', 0))
            time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            # Create table
            table = [
                ["Location", location],
                ["Date/Time", time_str],
                ["Condition", description.title()],
                ["Temperature", f"{temp}{temp_unit}"],
                ["Feels Like", f"{feels_like}{temp_unit}"],
                ["Humidity", f"{humidity}%"],
                ["Wind Speed", f"{wind_speed} {speed_unit}"]
            ]
            
            return tabulate(table, tablefmt="pretty")
            
        except Exception as e:
            logger.error(f"Error formatting weather data: {e}")
            return f"Error formatting weather data for {location}"

    def send_alert_email(self, location, alerts):
        """Send email notification for alerts."""
        if not self.email_config['enabled'] or not alerts:
            return
        
        try:
            msg = EmailMessage()
            msg['Subject'] = f"Weather Alert: {location}"
            msg['From'] = self.email_config['sender']
            msg['To'] = ', '.join(self.email_config['recipients'])
            
            content = [f"Weather Alerts for {location} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
            
            for alert in alerts:
                content.append(f"{alert['title']} ({alert['type'].upper()})")
                content.append(f"{alert['message']}")
                content.append("")
            
            msg.set_content('\n'.join(content))
            
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)
                
            logger.info(f"Alert email sent for {location}")
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")

    def check_locations(self):
        """Check weather for all configured locations."""
        for location in self.locations:
            logger.info(f"Checking weather for {location}")
            
            # Fetch current weather
            weather_data = self.get_current_weather(location)
            if not weather_data:
                logger.warning(f"No weather data received for {location}")
                continue
                
            # Display current weather
            print(f"\n{'-'*50}")
            print(self.format_weather_display(weather_data, location))
            
            # Generate and display alerts
            alerts = self.generate_alerts(weather_data)
            if alerts:
                print(f"\nALERTS FOR {location.upper()}:")
                for alert in alerts:
                    print(f"[{alert['type'].upper()}] {alert['title']}: {alert['message']}")
                
                # Send email notifications
                self.send_alert_email(location, alerts)
            else:
                print(f"\nNo weather alerts for {location}")
            
            print(f"{'-'*50}\n")

    def run_continuous(self, interval=3600):
        """Run the alert system continuously with specified interval."""
        logger.info(f"Starting continuous monitoring with {interval} seconds interval")
        
        try:
            while True:
                self.check_locations()
                logger.info(f"Sleeping for {interval} seconds before next check")
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Weather alert monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous monitoring: {e}")


def main():
    """Main function to run the Weather Alert System."""
    parser = argparse.ArgumentParser(description="Weather Alert System")
    parser.add_argument('-c', '--config', default='config.ini', help='Path to configuration file')
    parser.add_argument('-i', '--interval', type=int, default=3600, help='Check interval in seconds for continuous mode')
    parser.add_argument('-o', '--once', action='store_true', help='Run once and exit (no continuous monitoring)')
    args = parser.parse_args()
    
    try:
        weather_system = WeatherAlertSystem(config_file=args.config)
        
        if args.once:
            weather_system.check_locations()
        else:
            weather_system.run_continuous(interval=args.interval)
            
    except Exception as e:
        logger.error(f"Error running Weather Alert System: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())