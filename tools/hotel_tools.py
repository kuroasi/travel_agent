"""
Hotel search and booking related tool functions
"""
from datetime import datetime
from data.hotel_data import HOTELS, ROOM_TYPES, book_hotel_room, get_booking

def search_hotels(city=None, district=None, amenities=None, min_stars=None, max_price=None):
    """
    Search for hotel information

    Parameters:
    - city: City
    - district: District
    - amenities: List of facilities
    - min_stars: Minimum star rating
    - max_price: Maximum price (extracted from price range upper limit)

    Returns:
    - List of hotels matching the criteria
    """
    results = []

    for hotel in HOTELS:
        # Check city
        if city and hotel["city"] != city:
            continue

        # Check district
        if district and hotel["district"] != district:
            continue

        # Check amenities
        if amenities:
            if not all(amenity in hotel["amenities"] for amenity in amenities):
                continue

        # Check star rating
        if min_stars and hotel["stars"] < min_stars:
            continue

        # Check price range upper limit
        if max_price:
            price_range = hotel["price_range"].replace("¥", "").split("-")
            if len(price_range) > 1:
                max_hotel_price = int(price_range[1].replace(",", ""))
                if max_hotel_price > max_price:
                    continue

        # Add to results
        results.append({
            "hotel_id": hotel["hotel_id"],
            "name": hotel["name"],
            "city": hotel["city"],
            "district": hotel["district"],
            "address": hotel["address"],
            "stars": hotel["stars"],
            "rating": hotel["rating"],
            "amenities": hotel["amenities"],
            "description": hotel["description"],
            "price_range": hotel["price_range"]
        })

    if not results:
        return "No hotels found matching your criteria."

    # Format output
    formatted_results = "Found the following hotels matching your criteria:\n\n"
    for i, hotel in enumerate(results, 1):
        formatted_results += f"{i}. {hotel['name']} ({hotel['stars']} stars)\n"
        formatted_results += f"   Location: {hotel['district']}, {hotel['address']}\n"
        formatted_results += f"   Amenities: {', '.join(hotel['amenities'][:3])}...\n"
        formatted_results += f"   Price range: {hotel['price_range']}\n"
        formatted_results += f"   Rating: {hotel['rating']}\n"
        formatted_results += f"   Description: {hotel['description']}\n"
        formatted_results += f"   Hotel ID: {hotel['hotel_id']}\n\n"

    return formatted_results

def search_room_types(hotel_id, check_in_date=None, guests=None):
    """
    Query available room types for a hotel

    Parameters:
    - hotel_id: Hotel ID
    - check_in_date: Check-in date (optional)
    - guests: Number of guests (optional)

    Returns:
    - List of room types matching the criteria
    """
    # Verify if hotel ID exists
    hotel = None
    for h in HOTELS:
        if h["hotel_id"] == hotel_id:
            hotel = h
            break

    if not hotel:
        return "Hotel information not found."

    # Get room type information
    room_types = ROOM_TYPES.get(hotel_id, [])
    if not room_types:
        return f"No room type information found for {hotel['name']}."

    results = []
    for room in room_types:
        # Check if rooms are available
        if room["available"] <= 0:
            continue

        # Check guest capacity
        if guests and room["max_guests"] < guests:
            continue

        # Add to results
        results.append(room)

    if not results:
        return f"{hotel['name']} has no available rooms under the specified conditions."

    # Format output
    formatted_results = f"Available room types at {hotel['name']}:\n\n"
    for i, room in enumerate(results, 1):
        formatted_results += f"{i}. {room['name']}\n"
        formatted_results += f"   Room type ID: {room['type_id']}\n"
        formatted_results += f"   Bed type: {room['bed_type']}\n"
        formatted_results += f"   Area: {room['area']}\n"
        formatted_results += f"   View: {room['view']}\n"
        formatted_results += f"   Maximum occupancy: {room['max_guests']} persons\n"
        formatted_results += f"   Breakfast: {'Included' if room['breakfast'] else 'Not included'}\n"
        formatted_results += f"   Cancellation policy: {room['cancellation']}\n"
        formatted_results += f"   Amenities: {', '.join(room['amenities'])}\n"
        formatted_results += f"   Price: ¥{room['price']}/night\n"
        formatted_results += f"   Rooms available: {room['available']}\n\n"

    return formatted_results

def book_hotel(hotel_id, room_type_id, guest_name, id_number, phone,
               check_in_date, check_out_date):
    """
    Book a hotel room

    Parameters:
    - hotel_id: Hotel ID
    - room_type_id: Room type ID
    - guest_name: Guest name
    - id_number: ID card number
    - phone: Contact phone
    - check_in_date: Check-in date
    - check_out_date: Check-out date

    Returns:
    - Booking success information and booking ID, or reason for booking failure
    """
    # Verify if hotel ID exists
    hotel = None
    for h in HOTELS:
        if h["hotel_id"] == hotel_id:
            hotel = h
            break

    if not hotel:
        return "Booking failed: Hotel information not found."

    # Verify if room type ID exists
    room_type = None
    if hotel_id in ROOM_TYPES:
        for rt in ROOM_TYPES[hotel_id]:
            if rt["type_id"] == room_type_id:
                room_type = rt
                break

    if not room_type:
        return "Booking failed: Room type information not found."

    # Check if rooms are available
    if room_type["available"] <= 0:
        return "Booking failed: This room type is sold out."

    # Check check-in and check-out date format
    try:
        datetime.strptime(check_in_date, "%Y-%m-%d")
        datetime.strptime(check_out_date, "%Y-%m-%d")
    except ValueError:
        return "Booking failed: Incorrect date format, please use YYYY-MM-DD format."

    # Create booking
    booking_id = book_hotel_room(
        hotel_id,
        room_type_id,
        guest_name,
        id_number,
        phone,
        check_in_date,
        check_out_date
    )

    if not booking_id:
        return "Booking failed: System error, please try again later."
        
    # Get booking details
    booking = get_booking(booking_id)
    
    # Format booking success information
    result = "Booking successful! Here is your booking information:\n\n"
    result += f"Booking ID: {booking['booking_id']}\n"
    result += f"Hotel: {booking['hotel_name']}\n"
    result += f"Room type: {booking['room_type_name']}\n"
    result += f"Guest name: {booking['guest_name']}\n"
    result += f"Contact phone: {booking['phone']}\n"
    result += f"Check-in date: {booking['check_in_date']}\n"
    result += f"Check-out date: {booking['check_out_date']}\n"
    result += f"Room rate: ¥{booking['price']}/night\n"
    result += f"Booking status: {booking['status']}\n"
    result += f"Booking time: {booking['booking_time']}\n\n"
    result += "Thank you for choosing our service. We wish you a pleasant stay!"
    
    return result

def get_booking_info(booking_id):
    """
    Get booking information

    Parameters:
    - booking_id: Booking ID

    Returns:
    - Booking details or error message
    """
    booking = get_booking(booking_id)
    
    if not booking:
        return "No booking record found."
    
    # Format booking information
    result = "Booking details:\n\n"
    result += f"Booking ID: {booking['booking_id']}\n"
    result += f"Hotel: {booking['hotel_name']}\n"
    result += f"Room type: {booking['room_type_name']}\n"
    result += f"Guest name: {booking['guest_name']}\n"
    result += f"Contact phone: {booking['phone']}\n"
    result += f"Check-in date: {booking['check_in_date']}\n"
    result += f"Check-out date: {booking['check_out_date']}\n"
    result += f"Room rate: ¥{booking['price']}/night\n"
    result += f"Booking status: {booking['status']}\n"
    result += f"Booking time: {booking['booking_time']}\n"
    
    return result