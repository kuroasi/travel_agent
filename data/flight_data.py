"""
Simulated flight data for flight_agent demonstration
Contains virtual flight information, covering domestic and international flights
"""

flights = [
    # Domestic flights
    {
        "flight_id": "CA1234",
        "date": "2024-05-15",
        "departure_city": "Beijing",
        "departure_airport": "Capital International Airport (PEK)",
        "arrival_city": "Shanghai",
        "arrival_airport": "Pudong International Airport (PVG)",
        "departure_time": "08:30",
        "arrival_time": "10:45",
        "duration": "2 hours 15 minutes",
        "price": 1200,
        "airline": "Air China",
        "available_seats": 45,
        "cabin_class": "Economy"
    },
    {
        "flight_id": "MU5678",
        "date": "2024-05-15",
        "departure_city": "Beijing",
        "departure_airport": "Capital International Airport (PEK)",
        "arrival_city": "Shanghai",
        "arrival_airport": "Hongqiao International Airport (SHA)",
        "departure_time": "12:15",
        "arrival_time": "14:25",
        "duration": "2 hours 10 minutes",
        "price": 1350,
        "airline": "China Eastern Airlines",
        "available_seats": 0,
        "cabin_class": "Economy"
    },
    {
        "flight_id": "MU5678",
        "date": "2024-05-16",
        "departure_city": "Beijing",
        "departure_airport": "Capital International Airport (PEK)",
        "arrival_city": "Shanghai",
        "arrival_airport": "Hongqiao International Airport (SHA)",
        "departure_time": "12:15",
        "arrival_time": "14:25",
        "duration": "2 hours 10 minutes",
        "price": 1350,
        "airline": "China Eastern Airlines",
        "available_seats": 30,
        "cabin_class": "Economy"
    },
    {
        "flight_id": "CZ3456",
        "date": "2024-05-15",
        "departure_city": "Beijing",
        "departure_airport": "Capital International Airport (PEK)",
        "arrival_city": "Shanghai",
        "arrival_airport": "Hongqiao International Airport (SHA)",
        "departure_time": "10:00",
        "arrival_time": "12:30",
        "duration": "2 hours 30 minutes",
        "price": 8500,
        "airline": "China Southern Airlines",
        "available_seats": 25,
        "cabin_class": "Business"
    },
    {
        "flight_id": "CA1234",
        "date": "2024-05-17",
        "departure_city": "Shanghai",
        "departure_airport": "Pudong International Airport (PVG)",
        "arrival_city": "Beijing",
        "arrival_airport": "Capital International Airport (PEK)",
        "departure_time": "08:30",
        "arrival_time": "10:45",
        "duration": "2 hours 15 minutes",
        "price": 1300,
        "airline": "Air China",
        "available_seats": 55,
        "cabin_class": "Economy"
    },
    # International flights
    {
        "flight_id": "CA981",
        "date": "2024-05-15",
        "departure_city": "Beijing",
        "departure_airport": "Capital International Airport (PEK)",
        "arrival_city": "Tokyo",
        "arrival_airport": "Narita International Airport (NRT)",
        "departure_time": "09:30",
        "arrival_time": "13:45",
        "duration": "3 hours 15 minutes",
        "price": 6580,
        "airline": "Air China",
        "available_seats": 28,
        "cabin_class": "Economy"
    },
    {
        "flight_id": "MU507",
        "date": "2024-05-15",
        "departure_city": "Shanghai",
        "departure_airport": "Pudong International Airport (PVG)",
        "arrival_city": "Tokyo",
        "arrival_airport": "Narita International Airport (NRT)",
        "departure_time": "18:40",
        "arrival_time": "23:55",
        "duration": "3 hours 15 minutes",
        "price": 4850,
        "airline": "China Eastern Airlines",
        "available_seats": 32,
        "cabin_class": "Economy"
    },
    # International to international flights
    {
        "flight_id": "AF001",
        "date": "2024-05-15",
        "departure_city": "Paris",
        "departure_airport": "Charles de Gaulle Airport (CDG)",
        "arrival_city": "New York",
        "arrival_airport": "John F. Kennedy International Airport (JFK)",
        "departure_time": "10:30",
        "arrival_time": "13:00",
        "duration": "8 hours 30 minutes",
        "price": 5600,
        "airline": "Air France",
        "available_seats": 32,
        "cabin_class": "Economy"
    },
    {
        "flight_id": "BA019",
        "date": "2024-05-16",
        "departure_city": "New York",
        "departure_airport": "John F. Kennedy International Airport (JFK)",
        "arrival_city": "Paris",
        "arrival_airport": "Charles de Gaulle Airport (CDG)",
        "departure_time": "13:45",
        "arrival_time": "09:20",
        "duration": "8 hours 35 minutes",
        "price": 7200,
        "airline": "American Airlines",
        "available_seats": 28,
        "cabin_class": "Economy"
    },
    {
        "flight_id": "UA825",
        "date": "2024-05-17",
        "departure_city": "New York",
        "departure_airport": "John F. Kennedy International Airport (JFK)",
        "arrival_city": "Paris",
        "arrival_airport": "Charles de Gaulle Airport (CDG)",
        "departure_time": "22:30",
        "arrival_time": "06:45",
        "duration": "8 hours 15 minutes",
        "price": 9800,
        "airline": "United Airlines",
        "available_seats": 24,
        "cabin_class": "Economy"
    }
]

# Booking records
bookings = {}

def add_booking(booking_info):
    """Add booking record"""
    booking_id = f"B{len(bookings) + 1:04d}"
    bookings[booking_id] = booking_info
    bookings[booking_id]["booking_id"] = booking_id
    bookings[booking_id]["status"] = "Confirmed"
    return booking_id

def get_booking(booking_id):
    """Get booking information by booking ID"""
    return bookings.get(booking_id, None) 