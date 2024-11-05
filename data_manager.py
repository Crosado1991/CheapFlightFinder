import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for environment variables
SHEETY_USERNAME = os.getenv("ENV_SHEETY_USERNAME")
SHEETY_PASSWORD = os.getenv("ENV_SHEETY_PASSWORD")
SHEETY_PRICES_ENDPOINT = os.getenv("ENV_SHEETY_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.getenv("ENV_SHEETY_USERS_ENDPOINT")

class DataManager:
    def __init__(self):
        # Basic authentication and endpoints for Sheety
        self._user = SHEETY_USERNAME
        self._password = SHEETY_PASSWORD
        self.prices_endpoint = SHEETY_PRICES_ENDPOINT
        self.users_endpoint = SHEETY_USERS_ENDPOINT
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = []
        self.customer_data = []

    # Fetches destination data from the Google Sheet
    def get_destination_data(self):
        try:
            response = requests.get(url=self.prices_endpoint, auth=self._authorization)
            response.raise_for_status()
            data = response.json()

            if "prices" in data:
                self.destination_data = data["prices"]
                return self.destination_data
            else:
                print("Unexpected response structure:", data)
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data: {e}")
            return None

    # Updates destination IATA codes in the Google Sheet
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {"price": {"iataCode": city["iataCode"]}}

            try:
                response = requests.put(
                    url=f"{self.prices_endpoint}/{city['id']}",
                    json=new_data,
                    auth=self._authorization
                )
                response.raise_for_status()
                print(f"Successfully updated {city['city']}: {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"An error occurred while updating {city['city']}: {e}")

    # Fetches customer emails from the "Users" sheet in Google Sheets
    def get_customer_emails(self):
        try:
            response = requests.get(url=self.users_endpoint, auth=self._authorization)
            response.raise_for_status()
            data = response.json()
            if "users" in data:  # Ensure 'users' key exists
                self.customer_data = data["users"]
                return self.customer_data
            else:
                print("Unexpected response structure:", data)
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching customer emails: {e}")
            return None

    def add_user_to_sheet(self, first_name, last_name, email):
        new_user = {
            "user": {  # Changed from "users" to "user"
                "Whatisyourfirstname?": first_name,
                "Whatisyourlastname?": last_name,
                "Whatisyouremail?": email
            }
        }
        try:
            response = requests.post(url=self.users_endpoint, json=new_user, auth=self._authorization)
            response.raise_for_status()
            print(f"Successfully added user {first_name} {last_name} to the Google Sheet.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while adding user to sheet: {e}")

            print(f"Response: {response.text}")  # Log the response text for more info
