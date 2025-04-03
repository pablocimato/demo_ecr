# Weather App with Langchain and Gemini

This project is a command-line weather application that uses Langchain and Google's Gemini AI to provide weather information for any location. The app leverages OpenWeatherMap API to fetch current weather data.

## Features

- Get current weather information for any city or location
- Natural language processing with Google's Gemini AI
- Displays temperature, feels-like temperature, humidity, and weather description
- Spanish language support for weather descriptions

## Requirements

- Python 3.8+
- Required packages (see requirements.txt):
  - langchain
  - langchain-community
  - langchain-google-genai
  - google-generativeai
  - requests
  - python-dotenv

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with the following API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
   ```
   - Get a Google API key from [Google AI Studio](https://makersuite.google.com/)
   - Get an OpenWeatherMap API key from [OpenWeatherMap](https://openweathermap.org/api)

## Usage

Run the application with:
