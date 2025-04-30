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
        "price": 4580,
        "airline": "中国国际航空",
        "available_seats": 28,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "MU507",
        "date": "2024-05-15",
        "departure_city": "上海",
        "departure_airport": "浦东国际机场 (PVG)",
        "arrival_city": "新加坡",
        "arrival_airport": "樟宜机场 (SIN)",
        "departure_time": "18:40",
        "arrival_time": "23:55",
        "duration": "5小时15分钟",
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
        "departure_city": "伦敦",
        "departure_airport": "希思罗机场 (LHR)",
        "arrival_city": "东京",
        "arrival_airport": "成田国际机场 (NRT)",
        "departure_time": "13:45",
        "arrival_time": "09:20",
        "duration": "11小时35分钟",
        "price": 7200,
        "airline": "英国航空",
        "available_seats": 28,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "UA825",
        "date": "2024-05-17",
        "departure_city": "洛杉矶",
        "departure_airport": "洛杉矶国际机场 (LAX)",
        "arrival_city": "悉尼",
        "arrival_airport": "金斯福德史密斯机场 (SYD)",
        "departure_time": "22:30",
        "arrival_time": "06:45",
        "duration": "15小时15分钟",
        "price": 9800,
        "airline": "美国联合航空",
        "available_seats": 24,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "EK031",
        "date": "2024-05-18",
        "departure_city": "迪拜",
        "departure_airport": "迪拜国际机场 (DXB)",
        "arrival_city": "伦敦",
        "arrival_airport": "希思罗机场 (LHR)",
        "departure_time": "08:45",
        "arrival_time": "13:00",
        "duration": "7小时15分钟",
        "price": 6300,
        "airline": "阿联酋航空",
        "available_seats": 36,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "SQ321",
        "date": "2024-05-19",
        "departure_city": "新加坡",
        "departure_airport": "樟宜机场 (SIN)",
        "arrival_city": "法兰克福",
        "arrival_airport": "法兰克福国际机场 (FRA)",
        "departure_time": "23:55",
        "arrival_time": "06:40",
        "duration": "12小时45分钟",
        "price": 7500,
        "airline": "新加坡航空",
        "available_seats": 30,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "KE082",
        "date": "2024-05-20",
        "departure_city": "首尔",
        "departure_airport": "仁川国际机场 (ICN)",
        "arrival_city": "温哥华",
        "arrival_airport": "温哥华国际机场 (YVR)",
        "departure_time": "18:30",
        "arrival_time": "13:20",
        "duration": "9小时50分钟",
        "price": 8100,
        "airline": "大韩航空",
        "available_seats": 22,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "AZ610",
        "date": "2024-05-21",
        "departure_city": "罗马",
        "departure_airport": "菲乌米奇诺机场 (FCO)",
        "arrival_city": "纽约",
        "arrival_airport": "肯尼迪国际机场 (JFK)",
        "departure_time": "11:20",
        "arrival_time": "14:55",
        "duration": "9小时35分钟",
        "price": 6800,
        "airline": "意大利航空",
        "available_seats": 26,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "JL062",
        "date": "2024-05-22",
        "departure_city": "东京",
        "departure_airport": "成田国际机场 (NRT)",
        "arrival_city": "洛杉矶",
        "arrival_airport": "洛杉矶国际机场 (LAX)",
        "departure_time": "16:50",
        "arrival_time": "11:05",
        "duration": "10小时15分钟",
        "price": 8500,
        "airline": "日本航空",
        "available_seats": 34,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "QF001",
        "date": "2024-05-23",
        "departure_city": "悉尼",
        "departure_airport": "金斯福德史密斯机场 (SYD)",
        "arrival_city": "伦敦",
        "arrival_airport": "希思罗机场 (LHR)",
        "departure_time": "16:20",
        "arrival_time": "05:10",
        "duration": "23小时50分钟",
        "price": 12500,
        "airline": "澳洲航空",
        "available_seats": 20,
        "cabin_class": "经济舱"
    },
    {
        "flight_id": "SU2460",
        "date": "2024-05-24",
        "departure_city": "莫斯科",
        "departure_airport": "谢列梅捷沃国际机场 (SVO)",
        "arrival_city": "巴黎",
        "arrival_airport": "戴高乐机场 (CDG)",
        "departure_time": "09:20",
        "arrival_time": "11:55",
        "duration": "3小时35分钟",
        "price": 4200,
        "airline": "俄罗斯航空",
        "available_seats": 38,
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