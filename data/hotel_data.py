"""
Virtual hotel data and booking management
"""
from datetime import datetime, timedelta
import uuid

# Virtual hotel database
HOTELS = [
    {
        "hotel_id": "SH001",
        "name": "Waldorf Astoria Shanghai on the Bund",
        "city": "Shanghai",
        "district": "Huangpu District",
        "address": "No. 2 Zhongshan East 1st Road, Huangpu District",
        "stars": 5,
        "rating": 4.8,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Restaurant", "Bar", "Business Center", "Meeting Rooms"],
        "description": "Luxury hotel on the Shanghai Bund offering views of the Huangpu River and the Bund, with excellent facilities and service.",
        "image_url": "https://example.com/waldorf_shanghai.jpg",
        "price_range": "¥2,000-5,000"
    },
    {
        "hotel_id": "SH002",
        "name": "The Peninsula Shanghai",
        "city": "Shanghai",
        "district": "Huangpu District",
        "address": "No. 32 Zhongshan East 1st Road, Huangpu District",
        "stars": 5,
        "rating": 4.9,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Restaurant", "Bar", "Business Center", "Meeting Rooms", "Luxury Car Service"],
        "description": "A century-old classic hotel brand, located in the core area of the Bund, offering extremely luxurious rooms and world-class dining.",
        "image_url": "https://example.com/peninsula_shanghai.jpg",
        "price_range": "¥2,500-6,000"
    },
    {
        "hotel_id": "SH003",
        "name": "Shangri-La Pudong Shanghai",
        "city": "Shanghai",
        "district": "Pudong New District",
        "address": "No. 33 Fucheng Road, Pudong New District",
        "stars": 5,
        "rating": 4.7,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Restaurant", "Bar", "Business Center"],
        "description": "Luxury hotel in Pudong business district, close to Lujiazui Financial Center, offering quality service and facilities.",
        "image_url": "https://example.com/shangri_la_pudong.jpg",
        "price_range": "¥1,500-3,500"
    },
    {
        "hotel_id": "SH004",
        "name": "Shangri-La Jing'an Shanghai",
        "city": "Shanghai",
        "district": "Jing'an District",
        "address": "No. 1218 Nanjing West Road, Jing'an District",
        "stars": 5,
        "rating": 4.6,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Restaurant", "Bar"],
        "description": "High-end hotel in Jing'an Temple commercial area, convenient for shopping and dining, with comfortable and luxurious environment.",
        "image_url": "https://example.com/shangri_la_jing_an.jpg",
        "price_range": "¥1,400-3,200"
    },
    {
        "hotel_id": "SH005",
        "name": "Banyan Tree Shanghai on the Bund",
        "city": "Shanghai",
        "district": "Huangpu District",
        "address": "No. 558 Zhongshan East 1st Road, Huangpu District",
        "stars": 5,
        "rating": 4.8,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Restaurant", "Rooftop Bar"],
        "description": "Banyan Tree brand urban resort hotel, located on the Bund, offering spacious suites and high-end Spa experiences.",
        "image_url": "https://example.com/banyan_tree_shanghai.jpg",
        "price_range": "¥2,200-5,500"
    },
    {
        "hotel_id": "SH006",
        "name": "Peace Hotel Shanghai",
        "city": "Shanghai",
        "district": "Huangpu District",
        "address": "No. 20 Nanjing East Road, Huangpu District",
        "stars": 5,
        "rating": 4.5,
        "amenities": ["Swimming Pool", "Fitness Center", "Heritage Tour", "Restaurant", "Jazz Bar"],
        "description": "Historic Shanghai landmark, built in 1929, retaining classic decor style, providing guests with a memorable historical and cultural experience.",
        "image_url": "https://example.com/peace_hotel_shanghai.jpg",
        "price_range": "¥1,800-4,000"
    },
    {
        "hotel_id": "SH007",
        "name": "Bulgari Hotel Shanghai",
        "city": "Shanghai",
        "district": "Jing'an District",
        "address": "No. 33 Beijing West Road, Jing'an District",
        "stars": 5,
        "rating": 4.7,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Michelin Star Restaurant", "Bar"],
        "description": "Fashion boutique hotel created by luxury brand Bulgari, with strong design sense and high-quality dining experiences.",
        "image_url": "https://example.com/bulgari_shanghai.jpg",
        "price_range": "¥2,800-6,500"
    },
    {
        "hotel_id": "SH008",
        "name": "The Ritz-Carlton Pudong Shanghai",
        "city": "Shanghai",
        "district": "Pudong New District",
        "address": "No. 8 Century Avenue, Pudong New District",
        "stars": 5,
        "rating": 4.6,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Restaurant", "Executive Lounge"],
        "description": "Luxury hotel in Shanghai IFC, offering spectacular city views and refined service.",
        "image_url": "https://example.com/ritz_carlton_pudong.jpg",
        "price_range": "¥1,900-4,500"
    },
    {
        "hotel_id": "SH009",
        "name": "The Langham Xintiandi Shanghai",
        "city": "Shanghai",
        "district": "Huangpu District",
        "address": "No. 99 Madang Road, Huangpu District",
        "stars": 5,
        "rating": 4.5,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Chinese Restaurant", "Western Restaurant"],
        "description": "Modern luxury hotel in the historic Xintiandi area, blending Chinese and Western cultures.",
        "image_url": "https://example.com/langham_xintiandi.jpg",
        "price_range": "¥1,500-3,800"
    },
    {
        "hotel_id": "SH010",
        "name": "Andaz Shanghai",
        "city": "Shanghai",
        "district": "Jing'an District",
        "address": "No. 88 Shimen 1st Road, Jing'an District",
        "stars": 5,
        "rating": 4.6,
        "amenities": ["Rooftop Swimming Pool", "Fitness Center", "Spa", "Multiple Specialty Restaurants"],
        "description": "Hyatt's lifestyle hotel brand, located in the emerging Suhe Bay area, with strong design elements.",
        "image_url": "https://example.com/andaz_shanghai.jpg",
        "price_range": "¥1,600-3,500"
    },
    {
        "hotel_id": "SH011",
        "name": "Primus Hotel Hongqiao Shanghai",
        "city": "Shanghai",
        "district": "Minhang District",
        "address": "No. 2277 Hongqiao Road, Minhang District",
        "stars": 4,
        "rating": 4.3,
        "amenities": ["Fitness Center", "Restaurant", "Business Center", "Meeting Rooms"],
        "description": "Business hotel near Hongqiao Transportation Hub, with convenient transportation and comprehensive facilities.",
        "image_url": "https://example.com/primus_hongqiao.jpg",
        "price_range": "¥800-1,500"
    },
    {
        "hotel_id": "SH012",
        "name": "W Shanghai - The Bund",
        "city": "Shanghai",
        "district": "Huangpu District",
        "address": "No. 66 Zhongshan South Road, Huangpu District",
        "stars": 5,
        "rating": 4.5,
        "amenities": ["Swimming Pool", "Fitness Center", "Specialty Restaurant", "Bar", "Spa"],
        "description": "Trendy W Hotel brand, located on the South Bund, with modern design and vibrant atmosphere.",
        "image_url": "https://example.com/w_shanghai.jpg",
        "price_range": "¥1,700-3,800"
    },
    {
        "hotel_id": "SH013",
        "name": "Le Royal Meridien Shanghai",
        "city": "Shanghai",
        "district": "Pudong New District",
        "address": "No. 1288 Century Avenue, Pudong New District",
        "stars": 5,
        "rating": 4.4,
        "amenities": ["Indoor Swimming Pool", "Fitness Center", "Spa", "Multiple Restaurants"],
        "description": "Luxury hotel on Pudong Century Avenue, providing comfortable rooms and high-quality service.",
        "image_url": "https://example.com/le_royal_meridien.jpg",
        "price_range": "¥1,300-2,800"
    },
    {
        "hotel_id": "SH014",
        "name": "J Hotel Shanghai Tower",
        "city": "Shanghai",
        "district": "Pudong New District",
        "address": "No. 100 Century Avenue, Pudong New District",
        "stars": 5,
        "rating": 4.7,
        "amenities": ["World's Highest Hotel", "Infinity Pool", "Observation Deck", "Michelin Restaurant"],
        "description": "Ultra-high-rise hotel in Shanghai Tower, offering world-class views and service.",
        "image_url": "https://example.com/j_hotel_shanghai.jpg",
        "price_range": "¥2,500-8,000"
    },
    {
        "hotel_id": "SH015",
        "name": "Kerry Hotel Pudong Shanghai",
        "city": "Shanghai",
        "district": "Pudong New District",
        "address": "No. 1388 Huamu Road, Pudong New District",
        "stars": 5,
        "rating": 4.5,
        "amenities": ["Swimming Pool", "Fitness Center", "Spa", "Multiple Restaurants", "Connected to Shopping Mall"],
        "description": "Luxury business hotel connected to Kerry Center, offering convenient shopping and dining experiences.",
        "image_url": "https://example.com/kerry_pudong.jpg",
        "price_range": "¥1,200-2,600"
    }
]

# Room types for each hotel
ROOM_TYPES = {
    "SH001": [
        {
            "type_id": "SH001-DEL",
            "name": "Deluxe Room",
            "bed_type": "King Bed or Twin Beds",
            "area": "45 sq.m",
            "view": "City View",
            "max_guests": 2,
            "breakfast": True,
            "cancellation": "Free cancellation up to 24 hours before check-in",
            "amenities": ["Free Wi-Fi", "Minibar", "Safe", "Bathtub", "Shower", "Bathrobe", "Slippers"],
            "price": 2000,
            "available": 5
        },
        {
            "type_id": "SH001-RIV",
            "name": "River View Room",
            "bed_type": "King Bed",
            "area": "50 sq.m",
            "view": "Huangpu River View",
            "max_guests": 2,
            "breakfast": True,
            "cancellation": "Free cancellation up to 24 hours before check-in",
            "amenities": ["Free Wi-Fi", "Minibar", "Safe", "Bathtub", "Shower", "Bathrobe", "Slippers", "Evening Turn-down Service"],
            "price": 2800,
            "available": 3
        },
        {
            "type_id": "SH001-SUI",
            "name": "Luxury Suite",
            "bed_type": "King Bed",
            "area": "85 sq.m",
            "view": "Bund and River View",
            "max_guests": 3,
            "breakfast": True,
            "cancellation": "Free cancellation up to 48 hours before check-in",
            "amenities": ["Free Wi-Fi", "Living Room", "Dining Area", "Minibar", "Safe", "Bathtub", "Shower", "Bathrobe", "Slippers", "Butler Service"],
            "price": 5000,
            "available": 2
        }
    ],
    "SH002": [
        {
            "type_id": "SH002-DEL",
            "name": "Deluxe Room",
            "bed_type": "King Bed",
            "area": "55 sq.m",
            "view": "Garden View",
            "max_guests": 2,
            "breakfast": True,
            "cancellation": "Free cancellation up to 24 hours before check-in",
            "amenities": ["Free Wi-Fi", "Minibar", "Nespresso Machine", "Safe", "Bathtub", "Shower", "Bathrobe", "Slippers"],
            "price": 2500,
            "available": 4
        },
        {
            "type_id": "SH002-RIV",
            "name": "Deluxe River Room",
            "bed_type": "King Bed or Twin Beds",
            "area": "60 sq.m",
            "view": "Huangpu River View",
            "max_guests": 3,
            "breakfast": True,
            "cancellation": "Free cancellation up to 24 hours before check-in",
            "amenities": ["Free Wi-Fi", "Minibar", "Nespresso Machine", "Safe", "Bathtub", "Shower", "Bathrobe", "Slippers", "Butler Service"],
            "price": 3200,
            "available": 2
        },
        {
            "type_id": "SH002-SUI",
            "name": "Executive Suite",
            "bed_type": "King Bed",
            "area": "110 sq.m",
            "view": "Panoramic Bund View",
            "max_guests": 3,
            "breakfast": True,
            "cancellation": "Free cancellation up to 48 hours before check-in",
            "amenities": ["Free Wi-Fi", "Living Room", "Dining Area", "Minibar", "Nespresso Machine", "Safe", "Jacuzzi", "Shower", "Bathrobe", "Slippers", "Butler Service", "Luxury Car Service"],
            "price": 6000,
            "available": 1
        }
    ]
}

# Booking records
BOOKINGS = {}

def book_hotel_room(hotel_id, room_type_id, guest_name, id_number, phone, check_in_date, check_out_date):
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
    - Booking ID if successful, None if failed
    """
    # Verify the hotel and room type exist
    hotel_found = False
    room_type_found = False
    hotel_name = ""
    room_type_name = ""
    room_price = 0
    
    for hotel in HOTELS:
        if hotel["hotel_id"] == hotel_id:
            hotel_found = True
            hotel_name = hotel["name"]
            break
    
    if not hotel_found:
        return None
    
    if hotel_id not in ROOM_TYPES:
        return None
    
    for room_type in ROOM_TYPES[hotel_id]:
        if room_type["type_id"] == room_type_id:
            room_type_found = True
            room_type_name = room_type["name"]
            room_price = room_type["price"]
            
            # Check availability
            if room_type["available"] <= 0:
                return None
            
            # Update availability
            room_type["available"] -= 1
            break
    
    if not room_type_found:
        return None
    
    # Generate booking ID
    booking_id = f"B{uuid.uuid4().hex[:8].upper()}"
    
    # Create booking record
    BOOKINGS[booking_id] = {
        "booking_id": booking_id,
        "hotel_id": hotel_id,
        "hotel_name": hotel_name,
        "room_type_id": room_type_id,
        "room_type_name": room_type_name,
        "guest_name": guest_name,
        "id_number": id_number,
        "phone": phone,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "price": room_price,
        "status": "Confirmed",
        "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return booking_id

def get_booking(booking_id):
    """
    Get booking information by booking ID
    
    Parameters:
    - booking_id: Booking ID
    
    Returns:
    - Booking information if found, None if not found
    """
    return BOOKINGS.get(booking_id) 