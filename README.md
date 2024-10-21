# Real-Time Weather Monitoring System with Rollups and Aggregates

## Objective
This project implements a real-time data processing system that monitors weather conditions across major metros in India using the OpenWeatherMap API. It fetches weather data at regular intervals, processes it, stores the results in a database, and generates daily weather summaries. Additionally, it alerts users when predefined temperature thresholds are breached.

## Features
- Real-time weather data retrieval for Indian metros: Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad.
- Daily weather summaries:
  - Average, maximum, and minimum temperatures.
  - Dominant weather condition.
- User-defined alert thresholds for temperature or specific weather conditions.
- Visualization of historical weather data and trends.
- Storage of weather data and alerts in an SQLite database.

## Data Source
The data is sourced from the [OpenWeatherMap API](https://openweathermap.org/), which provides real-time weather information.

### Weather Parameters Used:
- **Main condition**: General weather condition (e.g., Clear, Rain, Snow).
- **Temperature**: Current temperature (in Celsius).
- **Feels Like**: Perceived temperature (in Celsius).
- **Timestamp**: Time of data update (Unix timestamp).

## Technologies Used
- **Programming Language**: Python
- **Database**: SQLite
- **API**: OpenWeatherMap
- **Visualization**: Matplotlib

## Setup Instructions

### Prerequisites
- **Python 3.x** installed on your system.
- An API key from OpenWeatherMap (you can get one [here](https://home.openweathermap.org/users/sign_up)).

### Libraries/Dependencies
Install the required Python libraries using `pip`:

```bash
pip install requests sqlite3 matplotlib
Setting up the Project
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/weather-monitoring-system.git
cd weather-monitoring-system
Configure the OpenWeatherMap API key:

Open the weather_monitoring.py file and set your API key:

python
Copy code
API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
Run the Application:

To start monitoring weather conditions:

bash
Copy code
python weather_monitoring.py
The system will fetch weather data for the configured cities every 5 minutes (configurable) and store the data in a SQLite database.

Design Choices
SQLite: Chosen for simplicity and ease of setup for persistent storage of weather data and alert logs.
Matplotlib: Used for generating visualizations of temperature trends and weather summaries.
Modular Design: Each function handles a specific task (data retrieval, processing, storage, alerting, visualization), making the system easy to extend or modify.
Features in Detail
1. Real-Time Data Retrieval
The system continuously fetches weather data from OpenWeatherMap for the specified cities every 5 minutes (or any configurable interval).
Temperature data is converted from Kelvin to Celsius (or Fahrenheit if preferred).
2. Rollups and Aggregates (Daily Summaries)
At the end of each day, the system calculates:
Average Temperature
Maximum Temperature
Minimum Temperature
Dominant Weather Condition (Based on the most frequent weather condition of the day)
These summaries are stored in the SQLite database for historical analysis.
3. Alerting Thresholds
User-configurable thresholds for temperature alerts.
Example: Trigger an alert if the temperature exceeds 35°C for two consecutive updates.
Alerts are logged in the database and displayed in the console.
4. Visualization
The visualize() function generates temperature trends for the last 7 days using Matplotlib.
You can plot historical weather data to observe trends over time for each city.
Configurable Settings
Polling Interval: The time interval (in seconds) between weather data updates.
Temperature Thresholds: You can set custom temperature thresholds for alerts.
Example Use Case
Real-time Monitoring: The system monitors current weather conditions in key cities and stores them in a database.
Daily Summaries: At the end of each day, rollups summarize temperature trends and dominant weather conditions for each city.
Alerting: If the temperature exceeds 35°C for two consecutive updates, the system triggers a temperature breach alert.
Visualizations: The user can visualize temperature trends for each city over the past week using the built-in plotting functionality.
Test Cases
System Setup: Verify the system starts successfully and connects to OpenWeatherMap API using a valid API key.
Data Retrieval: Ensure the system retrieves weather data for all configured cities at the specified interval and stores it correctly.
Temperature Conversion: Test Kelvin-to-Celsius conversion (or Fahrenheit if applicable).
Daily Weather Summary: Simulate a sequence of weather updates over several days and verify the calculation of daily averages, max/min temperatures, and dominant weather conditions.
Alerting Thresholds: Define and configure user thresholds for temperature alerts. Simulate weather data exceeding the thresholds and verify that alerts are triggered correctly.
Bonus Features
Extend the system to retrieve additional weather parameters (e.g., humidity, wind speed) from OpenWeatherMap API.
Retrieve weather forecasts and generate summaries based on predicted conditions.
Implement an email notification system for sending weather alerts.
Docker (Optional)
For users who prefer containerization, you can use Docker to run the application. Below is an example of how to set up a basic Docker container:

Build the Docker Image:

Create a Dockerfile:

dockerfile
Copy code
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "weather_monitoring.py"]
Build and Run the Container:

bash
Copy code
docker build -t weather-monitoring-system .
docker run weather-monitoring-system
Future Enhancements
Integrate advanced weather visualizations via a web dashboard (using Flask/Streamlit).
Implement push notifications for weather alerts.
Add support for more cities or regions.