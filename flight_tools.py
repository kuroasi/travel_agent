"""
航班查询和预订工具
定义两个主要工具：
1. 查询航班信息
2. 预订航班
"""

from langchain_core.tools import tool
from flight_data import flights, add_booking, get_booking

@tool
def search_flights(departure_city: str, arrival_city: str, date: str = None) -> str:
    """
    根据出发城市、到达城市和日期查询航班信息
    
    Args:
        departure_city: 出发城市
        arrival_city: 到达城市
        date: 航班日期 (可选，格式为YYYY-MM-DD)
        
    Returns:
        匹配的航班信息列表
    """
    # 清理和标准化输入参数
    departure_city = departure_city.strip()
    arrival_city = arrival_city.strip()
    
    # 过滤航班
    results = []
    
    # 首先尝试精确匹配
    for flight in flights:
        if (flight["departure_city"] == departure_city and 
            flight["arrival_city"] == arrival_city and
            (date is None or date == flight["date"])):
            results.append(flight)
    
    # 如果精确匹配没有结果，尝试部分匹配
    if not results:
        for flight in flights:
            if (departure_city in flight["departure_city"] and 
                arrival_city in flight["arrival_city"] and
                (date is None or date == flight["date"])):
                results.append(flight)
    
    # 格式化输出
    if not results:
        return f"未找到从{departure_city}到{arrival_city}的航班。" + (f"日期：{date}" if date else "")
    
    output = f"找到{len(results)}个从{departure_city}到{arrival_city}的航班" + (f"，日期：{date}" if date else "") + "\n\n"
    
    for flight in results:
        output += f"航班号: {flight['flight_id']} - {flight['airline']}\n"
        output += f"日期: {flight['date']}\n"
        output += f"路线: {flight['departure_city']}({flight['departure_airport']}) → {flight['arrival_city']}({flight['arrival_airport']})\n"
        output += f"时间: {flight['departure_time']} - {flight['arrival_time']} (飞行时间: {flight['duration']})\n"
        output += f"价格: ¥{flight['price']} ({flight['cabin_class']})\n"
        output += f"剩余座位: {flight['available_seats']}\n"
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
    预订指定航班
    
    Args:
        flight_id: 航班号码
        passenger_name: 乘客姓名
        passenger_id: 乘客身份证号
        contact_phone: 联系电话
        
    Returns:
        预订结果信息，包括预订号
    """
    # 查找航班
    selected_flight = None
    for flight in flights:
        if flight["flight_id"] == flight_id:
            selected_flight = flight
            break
    
    if not selected_flight:
        return f"未找到航班号为 {flight_id} 的航班，请核对后重试。"
    
    # 检查座位
    if selected_flight["available_seats"] <= 0:
        return f"抱歉，航班 {flight_id} 已无可用座位。"
    
    # 创建预订信息
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
    
    # 添加预订
    booking_id = add_booking(booking_info)
    
    # 更新航班座位数
    selected_flight["available_seats"] -= 1
    
    # 返回预订确认信息
    confirmation = f"✅ 预订成功！预订号: {booking_id}\n\n"
    confirmation += f"航班信息:\n"
    confirmation += f"- 航班号: {flight_id} ({selected_flight['airline']})\n"
    confirmation += f"- 日期: {selected_flight['date']}\n"
    confirmation += f"- 路线: {selected_flight['departure_city']} → {selected_flight['arrival_city']}\n"
    confirmation += f"- 起飞/到达: {selected_flight['departure_time']} - {selected_flight['arrival_time']}\n\n"
    confirmation += f"乘客信息:\n"
    confirmation += f"- 姓名: {passenger_name}\n"
    confirmation += f"- 证件号: {passenger_id}\n"
    confirmation += f"- 联系电话: {contact_phone}\n\n"
    confirmation += f"请在航班起飞前2小时到达机场办理登机手续。\n"
    confirmation += f"退改签规则请咨询航空公司客服。"
    
    return confirmation

@tool
def get_booking_info(booking_id: str) -> str:
    """
    根据预订号查询预订信息
    
    Args:
        booking_id: 预订号
        
    Returns:
        预订详情
    """
    booking = get_booking(booking_id)
    
    if not booking:
        return f"未找到预订号为 {booking_id} 的预订记录。"
    
    info = f"预订号: {booking_id} (状态: {booking['status']})\n\n"
    info += f"航班信息:\n"
    info += f"- 航班号: {booking['flight_id']} ({booking['airline']})\n"
    info += f"- 日期: {booking['date']}\n"
    info += f"- 路线: {booking['departure_city']} → {booking['arrival_city']}\n"
    info += f"- 起飞/到达: {booking['departure_time']} - {booking['arrival_time']}\n"
    info += f"- 机场: {booking['departure_airport']} → {booking['arrival_airport']}\n\n"
    info += f"乘客信息:\n"
    info += f"- 姓名: {booking['passenger_name']}\n"
    info += f"- 证件号: {booking['passenger_id']}\n"
    info += f"- 联系电话: {booking['contact_phone']}\n\n"
    info += f"票价: ¥{booking['price']} ({booking['cabin_class']})"
    
    return info 