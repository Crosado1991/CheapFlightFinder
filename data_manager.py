import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

SHEETY_USERNAME = os.getenv("ENV_SHEETY_USERNAME")
SHEETY_PASSWORD = os.getenv("ENV_SHEETY_PASSWORD")
SHEETY_PRICES_ENDPOINT = os.getenv("ENV_SHEETY_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.getenv("ENV_SHEETY_USERS_ENDPOINT")

class DataManager:
    def __init__(self):
        self._user = SHEETY_USERNAME
        self._password = SHEETY_PASSWORD
        self.prices_endpoint = SHEETY_PRICES_ENDPOINT
        self.users_endpoint = SHEETY_USERS_ENDPOINT
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = []
        self.customer_data = []

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

                if response.status_code == 200:
                    print(f"Successfully updated {city['city']}: {response.text}")
                else:
                    print(f"Failed to update {city['city']} with status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"An error occurred while updating {city['city']}: {e}")

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data

    def add_user_to_sheet(self, first_name, last_name, email):
        """Add a new user to the Google Sheet."""
        new_user = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
        try:
            response = requests.post(url=self.users_endpoint, json=new_user, auth=self._authorization)
            response.raise_for_status()
            if response.status_code == 201:
                print(f"Successfully added user {first_name} {last_name} to the Google Sheet.")
            else:
                print(f"Failed to add user: {response.status_code} {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while adding user to sheet: {e}")
