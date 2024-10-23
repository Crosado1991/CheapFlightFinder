# CheapFlightFinder
# Flight Price Tracker Application

This project is a Flight Price Tracker application designed to help users track and get notified about the cheapest flights between cities. It integrates with the Amadeus API for flight information and uses Sheety for managing user data in Google Sheets. Additionally, it sends notifications via WhatsApp (using Twilio API) and email for low-price alerts.

## Features
- Fetches flight data from the Amadeus API.
- Tracks price changes and sends notifications if the price drops below a threshold.
- Manages users' details using Google Sheets via Sheety API.
- Sends notifications via WhatsApp (Twilio) and email for price alerts.
- Built using `Tkinter` for a simple user interface to collect user information.

## Requirements
- Python 3.x
- Environment variables for API keys and secrets (Amadeus, Sheety, Twilio, SMTP)
- Required Python packages: `requests`, `tkinter`, `twilio`, `smtplib`, `dotenv`

## Project Structure
The project consists of the following Python modules:

### `data_manager.py`
Handles the interactions with the Sheety API for managing destination and user data.
- **Functions**:
  - `get_destination_data()`: Fetches flight destination data from Google Sheets.
  - `update_destination_codes()`: Updates IATA codes for destinations in Google Sheets.
  - `get_customer_emails()`: Retrieves customer emails from Google Sheets.
  - `add_user_to_sheet(first_name, last_name, email)`: Adds a new user to the Google Sheets.
  
### `flight_data.py`
Parses the flight data and manages the logic for finding the cheapest flight.
- **Classes**:
  - `FlightData`: A class that stores flight details such as price, origin, destination, etc.
- **Functions**:
  - `find_cheapest_flight(data)`: Identifies the cheapest flight option from the Amadeus API data.

### `flight_search.py`
Handles communication with the Amadeus API for fetching flight offers and IATA codes.
- **Functions**:
  - `get_destination_code(city_name)`: Retrieves the IATA code for a given city.
  - `check_flights(origin_city_code, destination_city_code, from_time, to_time, is_direct=True)`: Searches for flights between cities using the Amadeus API.

### `main.py`
The main logic that integrates the functionalities of the other modules. It performs the following:
- Collects user information using a `Tkinter` GUI and saves it to Google Sheets.
- Searches for the cheapest flight between destinations.
- Sends notifications via WhatsApp and email if flight prices drop below a threshold.

### `notification_manager.py`
Handles sending notifications to users via WhatsApp (Twilio API) and email (SMTP).
- **Functions**:
  - `send_whatsapp(message_body)`: Sends a WhatsApp message to notify users.
  - `send_emails(email_list, email_body)`: Sends an email notification to a list of users.

## Environment Variables
Ensure to set the following environment variables in your `.env` file:
- **Amadeus API**:
  - `ENV_AMA_API_KEY`: Amadeus API key.
  - `ENV_AMA_API_SECRET`: Amadeus API secret.
- **Sheety API**:
  - `ENV_SHEETY_USERNAME`: Sheety username.
  - `ENV_SHEETY_PASSWORD`: Sheety password.
  - `ENV_SHEETY_ENDPOINT`: Sheety endpoint for destination data.
  - `ENV_SHEETY_USERS_ENDPOINT`: Sheety endpoint for user data.
- **Twilio API**:
  - `ENV_TWILIO_WHATSAPP`: Twilio WhatsApp phone number.
  - `ENV_WHATSAPP_PHONE`: Verified WhatsApp number for sending messages.
  - `ENV_TWILIO_SID`: Twilio account SID.
  - `ENV_TWILIO_AUTH_TOKEN`: Twilio auth token.
- **SMTP for Emails**:
  - `ENV_SMTP`: SMTP provider's address (e.g., `smtp.gmail.com`).
  - `ENV_EMAIL`: Your email address.
  - `ENV_PASSWORD`: Your email password.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
Create a .env file and add your API credentials.
Run the application using:
bash
Copy code
python main.py
Usage
The application collects user information (first name, last name, and email) through a simple Tkinter form and stores it in a Google Sheet.
It then tracks the prices for flights from a predefined origin airport to the destination airports listed in the Google Sheet.
If a price falls below the stored threshold, the application sends an alert via WhatsApp and email.
