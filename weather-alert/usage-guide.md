# Weather Alert System - Usage Guide

This guide will help you set up and use the Python Weather Alert System.

## 1. Prerequisites

Before running the system, make sure you have:

- Python 3.6 or higher installed
- Required Python packages:
  - requests
  - tabulate
- An API key from OpenWeatherMap (free tier available)

## 2. Installation

1. Install the required packages:

```bash
pip install requests tabulate
```

2. Save the `weather_alert_system.py` script to your local machine.

3. Create a `config.ini` file in the same directory or use the default one that will be generated on first run.

## 3. Configuration

The system uses a configuration file (`config.ini`) for its settings. You can edit this file manually or it will be created with default values on the first run.

### API Configuration

```ini
[api]
key = YOUR_API_KEY_HERE
base_url = https://api.openweathermap.org/data/2.5
```

Replace `YOUR_API_KEY_HERE` with your OpenWeatherMap API key. You can get a free API key by signing up at [OpenWeatherMap](https://openweathermap.org/api).

### Locations to Monitor

```ini
[locations]
cities = ["New York", "Seattle", "Miami", "Denver"]
```

Add or remove cities as needed. Make sure to maintain the proper JSON array format.

### Alert Thresholds

```ini
[alerts]
temp_high = 95
temp_low = 32
wind_speed = 20
rain_probability = 70
```

Adjust these values based on your preferences:
- `temp_high`: High temperature threshold in °F or °C (based on your units setting)
- `temp_low`: Low temperature threshold in °F or °C
- `wind_speed`: Wind speed threshold in mph or m/s
- `rain_probability`: Rainfall probability threshold (percentage)

### Email Notifications

```ini
[email]
enabled = false
sender = your_email@gmail.com
recipients = ["recipient1@example.com", "recipient2@example.com"]
smtp_server = smtp.gmail.com
smtp_port = 587
username = your_email@gmail.com
password = your_app_password
```

To enable email notifications:
1. Set `enabled = true`
2. Fill in your email details
3. For Gmail, you'll need to use an app password instead of your regular password

## 4. Running the System

### One-time Check

To run a single check of all configured locations:

```bash
python weather_alert_system.py --once
```

### Continuous Monitoring

To run in continuous monitoring mode (default):

```bash
python weather_alert_system.py
```

This will check the weather based on the interval in your config file (default: 3600 seconds / 1 hour).

### Custom Configuration File

To use a custom configuration file:

```bash
python weather_alert_system.py --config my_custom_config.ini
```

### Custom Check Interval

To specify a custom check interval (in seconds) for continuous monitoring:

```bash
python weather_alert_system.py --interval 1800  # Check every 30 minutes
```

## 5. Understanding the Output

The system displays:
- Current weather conditions for each location
- Any alerts generated based on your configured thresholds
- Log messages about the system's operation

Sample output:
```
--------------------------------------------------
+------------+---------------------------+
| Location   | New York                  |
| Date/Time  | 2025-03-26 14:32:45      |
| Condition  | Partly Cloudy            |
| Temperature| 72.5°F                   |
| Feels Like | 70.3°F                   |
| Humidity   | 45%                      |
| Wind Speed | 8.5 mph                  |
+------------+---------------------------+

No weather alerts for New York
--------------------------------------------------
```

## 6. Troubleshooting

- If you receive API errors, verify your API key is correct and that you haven't exceeded your daily request limit.
- Check the `weather_alerts.log` file for detailed error messages.
- For email notification issues, ensure your email credentials are correct and that less secure app access is enabled (if using Gmail).

## 7. Advanced Use

### Environment Variables

Instead of storing your API key in the config file, you can set it as an environment variable:

```bash
export WEATHER_API_KEY="your_api_key_here"
python weather_alert_system.py
```

### System Service (Linux)

To run the system as a background service on Linux, create a systemd service file:

```
[Unit]
Description=Weather Alert System
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/weather_alert_system.py
WorkingDirectory=/path/to/directory
Restart=always
User=your_username

[Install]
WantedBy=multi-user.target
```

Save this to `/etc/systemd/system/weather-alert.service` and run:

```bash
sudo systemctl enable weather-alert.service
sudo systemctl start weather-alert.service
```