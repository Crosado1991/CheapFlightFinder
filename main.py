import time
from datetime import datetime, timedelta
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# ==================== Initialize Data Manager ====================
data_manager = DataManager()

# ==================== Set up Tkinter for User Input ====================

def submit_user_info():
    first_name = first_name_var.get()
    last_name = last_name_var.get()
    email = email_var.get()

    if not first_name or not last_name or not email:
        messagebox.showwarning("Input Error", "Please fill in all fields!")
        return

    # Save the user information to the Google Sheet
    data_manager.add_user_to_sheet(first_name, last_name, email)
    messagebox.showinfo("Success", "User information added successfully!")

    # Clear the fields after submission
    first_name_var.set("")
    last_name_var.set("")
    email_var.set("")

root = Tk()
root.title("Flight Price Tracker - User Information")

# Tkinter variables
first_name_var = StringVar()
last_name_var = StringVar()
email_var = StringVar()

# UI Labels and Entry fields
Label(root, text="What is your first name?").grid(row=0, column=0)
Entry(root, textvariable=first_name_var).grid(row=0, column=1)

Label(root, text="What is your last name?").grid(row=1, column=0)
Entry(root, textvariable=last_name_var).grid(row=1, column=1)

Label(root, text="What is your email?").grid(row=2, column=0)
Entry(root, textvariable=email_var).grid(row=2, column=1)

Button(root, text="Submit", command=submit_user_info).grid(row=3, column=1)

# Start the Tkinter loop
root.mainloop()

# ==================== Flight Price Tracker Logic ====================
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "PBI"  # Change to your desired origin

# Check if no destination data is available
if not sheet_data:
    print("No destination data available. Exiting program.")
    exit()

# ==================== Update the Airport Codes in Google Sheet ====================
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # Slowing down requests to avoid rate limit
        time.sleep(2)
print(f"Updated sheet data:\n{sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Retrieve your customer emails ====================
customer_data = data_manager.get_customer_emails()
customer_email_list = [row["What is your email?"] for row in customer_data]  # Ensure this is the correct key

# ==================== Search for Flights and Send Notifications ====================
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting direct flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)

    if not cheapest_flight or cheapest_flight.price == "N/A":
        print(f"No direct flights found for {destination['city']}. Skipping...")
        continue

    print(f"{destination['city']}: ${cheapest_flight.price}")
    time.sleep(2)

    if cheapest_flight.price == "N/A":
        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)

        if not cheapest_flight or cheapest_flight.price == "N/A":
            continue

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) departing on {cheapest_flight.out_date} " \
                      f"and returning on {cheapest_flight.return_date}."

        notification_manager.send_whatsapp(message_body=message)
        notification_manager.send_emails(email_list=customer_email_list, email_body=message)
