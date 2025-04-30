"""
Flight Search and Booking Tools
Defines two main tools:
1. Search for flight information
2. Book flights
"""

from langchain_core.tools import tool
from data.flight_data import flights, add_booking, get_booking

@tool
def search_flights(departure_city: str, arrival_city: str, date: str = None) -> str:
    """
    Search for flight information based on departure city, arrival city, and date

    Args:
        departure_city: Departure city
        arrival_city: Arrival city
        date: Flight date (optional, format is YYYY-MM-DD)

    Returns:
        List of matching flight information
    """
    # Clean and normalize input parameters
    departure_city = departure_city.strip()
    arrival_city = arrival_city.strip()

    # Filter flights
    results = []

    # First try exact matching
    for flight in flights:
        if (flight["departure_city"] == departure_city and
            flight["arrival_city"] == arrival_city and
            (date is None or date == flight["date"])):
            results.append(flight)

    # If exact matching has no results, try partial matching
    if not results:
        for flight in flights:
            if (departure_city in flight["departure_city"] and
                arrival_city in flight["arrival_city"] and
                (date is None or date == flight["date"])):
                results.append(flight)

    # Format output
    if not results:
        return f"No flights found from {departure_city} to {arrival_city}." + (f" Date: {date}" if date else "")

    output = f"Found {len(results)} flights from {departure_city} to {arrival_city}" + (f", date: {date}" if date else "") + "\n\n"

    for flight in results:
        output += f"Flight Number: {flight['flight_id']} - {flight['airline']}\n"
        output += f"Date: {flight['date']}\n"
        output += f"Route: {flight['departure_city']}({flight['departure_airport']}) → {flight['arrival_city']}({flight['arrival_airport']})\n"
        output += f"Time: {flight['departure_time']} - {flight['arrival_time']} (Flight duration: {flight['duration']})\n"
        output += f"Price: ¥{flight['price']} ({flight['cabin_class']})\n"
        output += f"Available seats: {flight['available_seats']}\n"
        output += "----------\n"

    return output

@tool
def book_flight(
    flight_id: str,
    passenger_name: str,
    passenger_id: str,
    contact_phone: str
) -> str:
    """
    Book a specified flight

    Args:
        flight_id: Flight number
        passenger_name: Passenger name
        passenger_id: Passenger ID number
        contact_phone: Contact phone number

    Returns:
        Booking result information, including booking number
    """
    # Find flight
    selected_flight = None
    for flight in flights:
        if flight["flight_id"] == flight_id:
            selected_flight = flight
            break

    if not selected_flight:
        return f"Flight number {flight_id} not found, please check and try again."

    # Check seats
    if selected_flight["available_seats"] <= 0:
        return f"Sorry, flight {flight_id} has no available seats."

    # Create booking information
    booking_info = {
        "flight_id": flight_id,
        "airline": selected_flight["airline"],
        "departure_city": selected_flight["departure_city"],
        "departure_airport": selected_flight["departure_airport"],
        "arrival_city": selected_flight["arrival_city"],
        "arrival_airport": selected_flight["arrival_airport"],
        "date": selected_flight["date"],
        "departure_time": selected_flight["departure_time"],
        "arrival_time": selected_flight["arrival_time"],
        "passenger_name": passenger_name,
        "passenger_id": passenger_id,
        "contact_phone": contact_phone,
        "price": selected_flight["price"],
        "cabin_class": selected_flight["cabin_class"]
    }

    # Add booking
    booking_id = add_booking(booking_info)

    # Update flight seats
    selected_flight["available_seats"] -= 1

    # Return booking confirmation
    confirmation = f"✅ Booking successful! Booking number: {booking_id}\n\n"
    confirmation += f"Flight information:\n"
    confirmation += f"- Flight number: {flight_id} ({selected_flight['airline']})\n"
    confirmation += f"- Date: {selected_flight['date']}\n"
    confirmation += f"- Route: {selected_flight['departure_city']} → {selected_flight['arrival_city']}\n"
    confirmation += f"- Departure/Arrival: {selected_flight['departure_time']} - {selected_flight['arrival_time']}\n\n"
    confirmation += f"Passenger information:\n"
    confirmation += f"- Name: {passenger_name}\n"
    confirmation += f"- ID number: {passenger_id}\n"
    confirmation += f"- Contact phone: {contact_phone}\n\n"
    confirmation += f"Please arrive at the airport 2 hours before the flight departure to check in.\n"
    confirmation += f"For rebooking and refund policies, please contact the airline customer service."

    return confirmation

@tool
def get_booking_info(booking_id: str) -> str:
    """
    Query booking information based on booking number

    Args:
        booking_id: Booking number

    Returns:
        Booking details
    """
    booking = get_booking(booking_id)

    if not booking:
        return f"No booking record found for booking number {booking_id}."

    info = f"Booking number: {booking_id} (Status: {booking['status']})\n\n"
    info += f"Flight information:\n"
    info += f"- Flight number: {booking['flight_id']} ({booking['airline']})\n"
    info += f"- Date: {booking['date']}\n"
    info += f"- Route: {booking['departure_city']} → {booking['arrival_city']}\n"
    info += f"- Departure/Arrival: {booking['departure_time']} - {booking['arrival_time']}\n"
    info += f"- Airports: {booking['departure_airport']} → {booking['arrival_airport']}\n\n"
    info += f"Passenger information:\n"
    info += f"- Name: {booking['passenger_name']}\n"
    info += f"- ID number: {booking['passenger_id']}\n"
    info += f"- Contact phone: {booking['contact_phone']}\n\n"
    info += f"Fare: ¥{booking['price']} ({booking['cabin_class']})"

    return info