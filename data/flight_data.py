"""
模拟航班数据，用于flight_agent演示
包含虚拟航班信息，涵盖国内和国际航班
"""

flights = [
    # 国内航班
    {
        "flight_id": "CA1234",
        "date": "2024-05-15",
        "departure_city": "北京",
        "departure_airport": "首都国际机场 (PEK)",
        "arrival_city": "上海",
        "arrival_airport": "浦东国际机场 (PVG)",
        "departure_time": "08:30",
        "arrival_time": "10:45",
        "duration": "2小时15分钟",
        "price": 1200,
        "airline": "中国国际航空",
        "available_seats": 45,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "MU5678",
        "date": "2024-05-15",
        "departure_city": "北京",
        "departure_airport": "首都国际机场 (PEK)",
        "arrival_city": "上海",
        "arrival_airport": "虹桥国际机场 (SHA)",
        "departure_time": "12:15",
        "arrival_time": "14:25",
        "duration": "2小时10分钟",
        "price": 1350,
        "airline": "东方航空",
        "available_seats": 0,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "MU5678",
        "date": "2024-05-16",
        "departure_city": "北京",
        "departure_airport": "首都国际机场 (PEK)",
        "arrival_city": "上海",
        "arrival_airport": "虹桥国际机场 (SHA)",
        "departure_time": "12:15",
        "arrival_time": "14:25",
        "duration": "2小时10分钟",
        "price": 1350,
        "airline": "东方航空",
        "available_seats": 30,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "CZ3456",
        "date": "2024-05-15",
        "departure_city": "北京",
        "departure_airport": "首都国际机场 (PEK)",
        "arrival_city": "上海",
        "arrival_airport": "虹桥国际机场 (SHA)",
        "departure_time": "10:00",
        "arrival_time": "12:30",
        "duration": "2小时30分钟",
        "price": 8500,
        "airline": "南方航空",
        "available_seats": 25,
        "cabin_class": "商务舱"
    },
    {
        "flight_id": "CA1234",
        "date": "2024-05-17",
        "departure_city": "上海",
        "departure_airport": "浦东国际机场 (PVG)",
        "arrival_city": "北京",
        "arrival_airport": "首都国际机场 (PEK)",
        "departure_time": "08:30",
        "arrival_time": "10:45",
        "duration": "2小时15分钟",
        "price": 1300,
        "airline": "中国国际航空",
        "available_seats": 55,
        "cabin_class": "经济舱"
    },
    # 国际航班
    {
        "flight_id": "CA981",
        "date": "2024-05-15",
        "departure_city": "北京",
        "departure_airport": "首都国际机场 (PEK)",
        "arrival_city": "东京",
        "arrival_airport": "成田国际机场 (NRT)",
        "departure_time": "09:30",
        "arrival_time": "13:45",
        "duration": "3小时15分钟",
        "price": 6580,
        "airline": "中国国际航空",
        "available_seats": 28,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "MU507",
        "date": "2024-05-15",
        "departure_city": "上海",
        "departure_airport": "浦东国际机场 (PVG)",
        "arrival_city": "东京",
        "arrival_airport": "成田国际机场 (NRT)",
        "departure_time": "18:40",
        "arrival_time": "23:55",
        "duration": "3小时15分钟",
        "price": 4850,
        "airline": "东方航空",
        "available_seats": 32,
        "cabin_class": "经济舱"
    },
    # 国际间航班（国外到国外）
    {
        "flight_id": "AF001",
        "date": "2024-05-15",
        "departure_city": "巴黎",
        "departure_airport": "戴高乐机场 (CDG)",
        "arrival_city": "纽约",
        "arrival_airport": "肯尼迪国际机场 (JFK)",
        "departure_time": "10:30",
        "arrival_time": "13:00",
        "duration": "8小时30分钟",
        "price": 5600,
        "airline": "法国航空",
        "available_seats": 32,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "BA019",
        "date": "2024-05-16",
        "departure_city": "纽约",
        "departure_airport": "肯尼迪国际机场 (JFK)",
        "arrival_city": "巴黎",
        "arrival_airport": "戴高乐机场 (CDG)",
        "departure_time": "13:45",
        "arrival_time": "09:20",
        "duration": "8小时35分钟",
        "price": 7200,
        "airline": "美国航空",
        "available_seats": 28,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "UA825",
        "date": "2024-05-17",
        "departure_city": "纽约",
        "departure_airport": "肯尼迪国际机场 (JFK)",
        "arrival_city": "巴黎",
        "arrival_airport": "戴高乐机场 (CDG)",
        "departure_time": "22:30",
        "arrival_time": "06:45",
        "duration": "8小时15分钟",
        "price": 9800,
        "airline": "美国联合航空",
        "available_seats": 24,
        "cabin_class": "经济舱"
    }
]

# 预订记录
bookings = {}

def add_booking(booking_info):
    """添加预订记录"""
    booking_id = f"B{len(bookings) + 1:04d}"
    bookings[booking_id] = booking_info
    bookings[booking_id]["booking_id"] = booking_id
    bookings[booking_id]["status"] = "已确认"
    return booking_id

def get_booking(booking_id):
    """根据预订ID获取预订信息"""
    return bookings.get(booking_id, None) 