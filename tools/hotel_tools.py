"""
酒店查询和预订相关工具函数
"""
from datetime import datetime
from data.hotel_data import HOTELS, ROOM_TYPES, book_hotel_room, get_booking

def search_hotels(city=None, district=None, amenities=None, min_stars=None, max_price=None):
    """
    查询酒店信息

    参数:
    - city: 城市
    - district: 区域
    - amenities: 设施列表
    - min_stars: 最低星级
    - max_price: 最高价格(从价格区间提取上限)

    返回:
    - 符合条件的酒店列表
    """
    results = []

    for hotel in HOTELS:
        # 检查城市
        if city and hotel["city"] != city:
            continue

        # 检查区域
        if district and hotel["district"] != district:
            continue

        # 检查设施
        if amenities:
            if not all(amenity in hotel["amenities"] for amenity in amenities):
                continue

        # 检查星级
        if min_stars and hotel["stars"] < min_stars:
            continue

        # 检查价格区间上限
        if max_price:
            price_range = hotel["price_range"].replace("¥", "").split("-")
            if len(price_range) > 1:
                max_hotel_price = int(price_range[1].replace(",", ""))
                if max_hotel_price > max_price:
                    continue

        # 添加到结果
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
        return "未找到符合条件的酒店。"

    # 格式化输出
    formatted_results = "找到以下符合条件的酒店：\n\n"
    for i, hotel in enumerate(results, 1):
        formatted_results += f"{i}. {hotel['name']} ({hotel['stars']}星级)\n"
        formatted_results += f"   位置: {hotel['district']}, {hotel['address']}\n"
        formatted_results += f"   设施: {', '.join(hotel['amenities'][:3])}...\n"
        formatted_results += f"   价格区间: {hotel['price_range']}\n"
        formatted_results += f"   评分: {hotel['rating']}\n"
        formatted_results += f"   简介: {hotel['description']}\n"
        formatted_results += f"   酒店ID: {hotel['hotel_id']}\n\n"

    return formatted_results

def search_room_types(hotel_id, check_in_date=None, guests=None):
    """
    查询酒店可用房型

    参数:
    - hotel_id: 酒店ID
    - check_in_date: 入住日期 (可选)
    - guests: 入住人数 (可选)

    返回:
    - 符合条件的房型列表
    """
    # 验证酒店ID是否存在
    hotel = None
    for h in HOTELS:
        if h["hotel_id"] == hotel_id:
            hotel = h
            break

    if not hotel:
        return "未找到该酒店信息。"

    # 获取房型信息
    room_types = ROOM_TYPES.get(hotel_id, [])
    if not room_types:
        return f"未找到{hotel['name']}的房型信息。"

    results = []
    for room in room_types:
        # 检查是否有可用房间
        if room["available"] <= 0:
            continue

        # 检查入住人数
        if guests and room["max_guests"] < guests:
            continue

        # 添加到结果
        results.append(room)

    if not results:
        return f"{hotel['name']}在指定条件下没有可用房间。"

    # 格式化输出
    formatted_results = f"{hotel['name']}可用房型信息：\n\n"
    for i, room in enumerate(results, 1):
        formatted_results += f"{i}. {room['name']}\n"
        formatted_results += f"   房型ID: {room['type_id']}\n"
        formatted_results += f"   床型: {room['bed_type']}\n"
        formatted_results += f"   面积: {room['area']}\n"
        formatted_results += f"   景观: {room['view']}\n"
        formatted_results += f"   最多入住: {room['max_guests']}人\n"
        formatted_results += f"   早餐: {'含早' if room['breakfast'] else '不含早'}\n"
        formatted_results += f"   取消政策: {room['cancellation']}\n"
        formatted_results += f"   设施: {', '.join(room['amenities'])}\n"
        formatted_results += f"   价格: ¥{room['price']}/晚\n"
        formatted_results += f"   剩余房间数: {room['available']}\n\n"

    return formatted_results

def book_hotel(hotel_id, room_type_id, guest_name, id_number, phone,
               check_in_date, check_out_date):
    """
    预订酒店

    参数:
    - hotel_id: 酒店ID
    - room_type_id: 房型ID
    - guest_name: 客人姓名
    - id_number: 身份证号
    - phone: 联系电话
    - check_in_date: 入住日期
    - check_out_date: 退房日期

    返回:
    - 预订成功信息和预订号，或预订失败原因
    """
    # 验证酒店ID是否存在
    hotel = None
    for h in HOTELS:
        if h["hotel_id"] == hotel_id:
            hotel = h
            break

    if not hotel:
        return "预订失败：未找到该酒店信息。"

    # 验证房型ID是否存在
    room_type = None
    if hotel_id in ROOM_TYPES:
        for rt in ROOM_TYPES[hotel_id]:
            if rt["type_id"] == room_type_id:
                room_type = rt
                break

    if not room_type:
        return "预订失败：未找到该房型信息。"

    # 检查是否有可用房间
    if room_type["available"] <= 0:
        return "预订失败：该房型已售罄。"

    # 检查入住日期和退房日期格式
    try:
        datetime.strptime(check_in_date, "%Y-%m-%d")
        datetime.strptime(check_out_date, "%Y-%m-%d")
    except ValueError:
        return "预订失败：日期格式不正确，请使用YYYY-MM-DD格式。"

    # 创建预订
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
        return "预订失败：系统错误，请稍后重试。"

    # 获取预订详情
    booking = get_booking(booking_id)

    # 格式化预订成功信息
    result = "预订成功！以下是您的预订信息：\n\n"
    result += f"预订号: {booking['booking_id']}\n"
    result += f"酒店名称: {booking['hotel_name']}\n"
    result += f"房型: {booking['room_type_name']}\n"
    result += f"入住人: {booking['guest_name']}\n"
    result += f"联系电话: {booking['phone']}\n"
    result += f"入住日期: {booking['check_in_date']}\n"
    result += f"退房日期: {booking['check_out_date']}\n"
    result += f"房费: ¥{booking['price']}/晚\n"
    result += f"预订状态: {booking['status']}\n"
    result += f"预订时间: {booking['booking_time']}\n\n"
    result += "感谢您选择我们的服务，祝您旅途愉快！"

    return result

def get_booking_info(booking_id):
    """
    获取预订信息

    参数:
    - booking_id: 预订号

    返回:
    - 预订详情或错误信息
    """
    booking = get_booking(booking_id)

    if not booking:
        return "未找到该预订记录。"

    # 格式化预订信息
    result = "预订详情：\n\n"
    result += f"预订号: {booking['booking_id']}\n"
    result += f"酒店名称: {booking['hotel_name']}\n"
    result += f"房型: {booking['room_type_name']}\n"
    result += f"入住人: {booking['guest_name']}\n"
    result += f"联系电话: {booking['phone']}\n"
    result += f"入住日期: {booking['check_in_date']}\n"
    result += f"退房日期: {booking['check_out_date']}\n"
    result += f"房费: ¥{booking['price']}/晚\n"
    result += f"预订状态: {booking['status']}\n"
    result += f"预订时间: {booking['booking_time']}\n"

    return result