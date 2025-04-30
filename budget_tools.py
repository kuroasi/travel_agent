"""
旅行预算管理相关工具函数
"""
from datetime import datetime
import uuid

# 保存用户预算和支出的数据结构
TRAVEL_BUDGETS = {}
EXPENSES = {}

def estimate_travel_budget(destination, days, traveler_count, travel_style="标准"):
    """
    估算旅行总预算
    
    参数:
    - destination: 目的地，如"上海"、"东京"
    - days: 旅行天数
    - traveler_count: 旅行人数
    - travel_style: 旅行风格，可选"经济"、"标准"、"豪华"
    
    返回:
    - 预算估算结果，包括总预算和各项明细
    """
    # 不同旅行风格的基础花费(每人每天)
    base_costs = {
        "经济": {"住宿": 300, "餐饮": 150, "交通": 100, "景点": 100, "购物": 200, "其他": 50},
        "标准": {"住宿": 600, "餐饮": 300, "交通": 150, "景点": 150, "购物": 500, "其他": 100},
        "豪华": {"住宿": 1500, "餐饮": 600, "交通": 300, "景点": 300, "购物": 1000, "其他": 300}
    }
    
    # 特定城市的调整系数
    city_factors = {
        "上海": 1.2, "北京": 1.1, "广州": 1.0, "深圳": 1.1, "杭州": 1.0,
        "东京": 1.5, "大阪": 1.3, "京都": 1.3, "首尔": 1.2, "曼谷": 0.8,
        "新加坡": 1.4, "香港": 1.5, "纽约": 1.8, "巴黎": 1.6, "伦敦": 1.7,
        "罗马": 1.5, "悉尼": 1.5, "迪拜": 1.6, "马尔代夫": 2.0
    }
    
    # 获取城市系数，如果不在列表中则默认为1.0
    city_factor = city_factors.get(destination, 1.0)
    
    # 获取基础花费
    base = base_costs.get(travel_style, base_costs["标准"])
    
    # 计算各项预算
    budget_items = {}
    total_budget = 0
    
    for category, daily_cost in base.items():
        # 应用城市系数和人数、天数
        category_cost = daily_cost * city_factor * traveler_count * days
        budget_items[category] = round(category_cost)
        total_budget += category_cost
    
    # 往返机票估算(每人)
    flight_costs = {
        "国内": {"经济": 1500, "标准": 2500, "豪华": 5000},
        "亚洲": {"经济": 3000, "标准": 5000, "豪华": 12000},
        "欧美": {"经济": 6000, "标准": 10000, "豪华": 25000}
    }
    
    # 根据目的地判断大致区域
    if destination in ["上海", "北京", "广州", "深圳", "杭州"]:
        region = "国内"
    elif destination in ["东京", "大阪", "京都", "首尔", "曼谷", "新加坡", "香港"]:
        region = "亚洲"
    else:
        region = "欧美"
    
    # 添加机票预算
    flight_budget = flight_costs[region][travel_style] * traveler_count
    budget_items["机票"] = flight_budget
    total_budget += flight_budget
    
    # 生成预算ID并保存预算信息
    budget_id = f"B{uuid.uuid4().hex[:8].upper()}"
    
    TRAVEL_BUDGETS[budget_id] = {
        "budget_id": budget_id,
        "destination": destination,
        "days": days,
        "traveler_count": traveler_count,
        "travel_style": travel_style,
        "total_budget": round(total_budget),
        "budget_items": budget_items,
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 格式化输出
    result = f"旅行预算估算 (ID: {budget_id}):\n\n"
    result += f"目的地: {destination}\n"
    result += f"旅行天数: {days}天\n"
    result += f"旅行人数: {traveler_count}人\n"
    result += f"旅行风格: {travel_style}\n\n"
    
    result += "预算明细:\n"
    for category, amount in budget_items.items():
        result += f"- {category}: ¥{amount:,}\n"
    
    result += f"\n总预算: ¥{round(total_budget):,}\n"
    result += f"人均预算: ¥{round(total_budget/traveler_count):,}\n"
    result += f"人均每日预算: ¥{round(total_budget/traveler_count/days):,}\n"
    
    return result

def track_expense(budget_id, category, amount, description=None):
    """
    记录旅行支出
    
    参数:
    - budget_id: 预算ID
    - category: 支出类别，如"住宿"、"餐饮"、"交通"等
    - amount: 支出金额
    - description: 支出描述(可选)
    
    返回:
    - 支出记录确认和剩余预算信息
    """
    # 检查预算ID是否存在
    if budget_id not in TRAVEL_BUDGETS:
        return "无法找到该预算ID，请确认后重试。"
    
    budget = TRAVEL_BUDGETS[budget_id]
    
    # 检查类别是否有效
    valid_categories = list(budget["budget_items"].keys())
    if category not in valid_categories:
        return f"无效的支出类别。请使用以下类别之一: {', '.join(valid_categories)}"
    
    # 生成支出ID
    expense_id = f"E{uuid.uuid4().hex[:8].upper()}"
    
    # 记录支出
    if budget_id not in EXPENSES:
        EXPENSES[budget_id] = []
    
    EXPENSES[budget_id].append({
        "expense_id": expense_id,
        "category": category,
        "amount": amount,
        "description": description,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # 计算该类别已用预算和剩余预算
    category_budget = budget["budget_items"][category]
    category_spent = sum(e["amount"] for e in EXPENSES[budget_id] if e["category"] == category)
    category_remaining = category_budget - category_spent
    
    # 计算总体已用预算和剩余预算
    total_budget = budget["total_budget"]
    total_spent = sum(e["amount"] for e in EXPENSES[budget_id])
    total_remaining = total_budget - total_spent
    
    # 格式化输出
    result = "支出已记录!\n\n"
    result += f"支出ID: {expense_id}\n"
    result += f"类别: {category}\n"
    result += f"金额: ¥{amount:,}\n"
    
    if description:
        result += f"描述: {description}\n"
    
    result += f"\n{category}类别预算: ¥{category_budget:,}\n"
    result += f"{category}类别已花费: ¥{category_spent:,}\n"
    result += f"{category}类别剩余: ¥{category_remaining:,} "
    
    # 添加预算使用百分比
    category_percent = (category_spent / category_budget) * 100
    result += f"({category_percent:.1f}%已使用)\n\n"
    
    result += f"总预算: ¥{total_budget:,}\n"
    result += f"总支出: ¥{total_spent:,}\n"
    result += f"剩余预算: ¥{total_remaining:,} "
    
    # 添加总预算使用百分比
    total_percent = (total_spent / total_budget) * 100
    result += f"({total_percent:.1f}%已使用)"
    
    return result

def analyze_budget(budget_id):
    """
    分析预算使用情况
    
    参数:
    - budget_id: 预算ID
    
    返回:
    - 预算使用分析报告
    """
    # 检查预算ID是否存在
    if budget_id not in TRAVEL_BUDGETS:
        return "无法找到该预算ID，请确认后重试。"
    
    budget = TRAVEL_BUDGETS[budget_id]
    
    # 检查是否有支出记录
    if budget_id not in EXPENSES or not EXPENSES[budget_id]:
        return f"尚未记录任何支出。预算总额: ¥{budget['total_budget']:,}"
    
    # 计算各类别的支出和剩余
    categories = {}
    total_spent = 0
    
    for category, budget_amount in budget["budget_items"].items():
        spent = sum(e["amount"] for e in EXPENSES[budget_id] if e["category"] == category)
        remaining = budget_amount - spent
        percent_used = (spent / budget_amount) * 100 if budget_amount > 0 else 0
        
        categories[category] = {
            "budget": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "percent_used": percent_used
        }
        
        total_spent += spent
    
    total_budget = budget["total_budget"]
    total_remaining = total_budget - total_spent
    total_percent_used = (total_spent / total_budget) * 100
    
    # 格式化输出
    result = f"预算分析报告 (ID: {budget_id}):\n\n"
    result += f"目的地: {budget['destination']}\n"
    result += f"旅行天数: {budget['days']}天\n"
    result += f"旅行人数: {budget['traveler_count']}人\n"
    result += f"旅行风格: {budget['travel_style']}\n\n"
    
    # 添加总体预算情况
    result += "总体预算情况:\n"
    result += f"总预算: ¥{total_budget:,}\n"
    result += f"已花费: ¥{total_spent:,} ({total_percent_used:.1f}%)\n"
    result += f"剩余预算: ¥{total_remaining:,} ({100-total_percent_used:.1f}%)\n\n"
    
    # 添加各类别预算使用情况
    result += "各类别预算使用情况:\n"
    
    # 按使用百分比排序
    sorted_categories = sorted(categories.items(), key=lambda x: x[1]["percent_used"], reverse=True)
    
    for category, data in sorted_categories:
        result += f"- {category}:\n"
        result += f"  预算: ¥{data['budget']:,}\n"
        result += f"  已花费: ¥{data['spent']:,} ({data['percent_used']:.1f}%)\n"
        result += f"  剩余: ¥{data['remaining']:,}\n"
    
    # 添加预算建议
    result += "\n预算建议:\n"
    
    # 超支类别
    over_budget = [c for c, d in categories.items() if d["percent_used"] > 100]
    if over_budget:
        result += f"- 以下类别已超出预算: {', '.join(over_budget)}\n"
    
    # 接近超支类别
    near_limit = [c for c, d in categories.items() if 80 <= d["percent_used"] <= 100]
    if near_limit:
        result += f"- 以下类别接近预算上限: {', '.join(near_limit)}\n"
    
    # 充足预算类别
    good_categories = [c for c, d in categories.items() if d["percent_used"] < 50]
    if good_categories:
        result += f"- 以下类别预算充足: {', '.join(good_categories)}\n"
    
    # 总体预算状况评估
    if total_percent_used > 90:
        result += "- 总体预算即将用尽，建议控制后续支出\n"
    elif total_percent_used > 70:
        result += "- 总体预算使用较多，建议适当控制后续支出\n"
    else:
        result += "- 总体预算状况良好，可以继续按计划使用\n"
    
    return result

def compare_options(option_type, options):
    """
    比较不同选项的成本和价值
    
    参数:
    - option_type: 选项类型，如"酒店"、"交通"等
    - options: 选项列表，格式为[{"name": "选项1", "cost": 1000, "features": ["特点1", "特点2"]}, ...]
    
    返回:
    - 选项比较分析
    """
    if not options or len(options) < 2:
        return "请提供至少两个选项进行比较。"
    
    # 按成本排序选项
    sorted_options = sorted(options, key=lambda x: x["cost"])
    
    # 计算最便宜和最贵选项之间的价差和百分比
    cheapest = sorted_options[0]
    most_expensive = sorted_options[-1]
    price_diff = most_expensive["cost"] - cheapest["cost"]
    price_diff_percent = (price_diff / cheapest["cost"]) * 100 if cheapest["cost"] > 0 else 0
    
    # 格式化输出
    result = f"{option_type}选项比较:\n\n"
    
    for i, option in enumerate(sorted_options, 1):
        result += f"{i}. {option['name']}\n"
        result += f"   价格: ¥{option['cost']:,}\n"
        
        if "features" in option and option["features"]:
            result += f"   特点: {', '.join(option['features'])}\n"
        
        if i > 1:
            diff = option["cost"] - sorted_options[0]["cost"]
            diff_percent = (diff / sorted_options[0]["cost"]) * 100 if sorted_options[0]["cost"] > 0 else 0
            result += f"   比最便宜选项贵: ¥{diff:,} ({diff_percent:.1f}%)\n"
        
        result += "\n"
    
    # 添加总体分析
    result += "分析:\n"
    result += f"- 价格范围: ¥{cheapest['cost']:,} 至 ¥{most_expensive['cost']:,}\n"
    result += f"- 最高价与最低价差异: ¥{price_diff:,} ({price_diff_percent:.1f}%)\n"
    
    # 添加针对性建议
    result += "\n建议:\n"
    
    if price_diff_percent < 20:
        result += "- 各选项价格差异不大，建议选择性价比最高的选项\n"
    elif price_diff_percent > 100:
        result += "- 价格差异显著，请仔细评估更贵选项是否值得投入额外费用\n"
    else:
        result += "- 价格差异适中，请根据您的预算和需求选择合适选项\n"
    
    return result

def get_budget_summary(budget_id=None):
    """
    获取预算摘要信息
    
    参数:
    - budget_id: 预算ID（可选，不提供则返回所有预算摘要）
    
    返回:
    - 预算摘要信息
    """
    # 如果没有预算记录
    if not TRAVEL_BUDGETS:
        return "尚未创建任何旅行预算。"
    
    # 如果指定了预算ID
    if budget_id:
        if budget_id not in TRAVEL_BUDGETS:
            return "无法找到该预算ID，请确认后重试。"
        
        budgets_to_show = {budget_id: TRAVEL_BUDGETS[budget_id]}
    else:
        budgets_to_show = TRAVEL_BUDGETS
    
    # 格式化输出
    result = "旅行预算摘要:\n\n"
    
    for bid, budget in budgets_to_show.items():
        result += f"预算ID: {bid}\n"
        result += f"目的地: {budget['destination']}\n"
        result += f"天数/人数: {budget['days']}天/{budget['traveler_count']}人\n"
        result += f"旅行风格: {budget['travel_style']}\n"
        result += f"总预算: ¥{budget['total_budget']:,}\n"
        
        # 如果有支出记录，计算已用和剩余预算
        if bid in EXPENSES and EXPENSES[bid]:
            total_spent = sum(e["amount"] for e in EXPENSES[bid])
            total_remaining = budget["total_budget"] - total_spent
            percent_used = (total_spent / budget["total_budget"]) * 100
            
            result += f"已花费: ¥{total_spent:,} ({percent_used:.1f}%)\n"
            result += f"剩余预算: ¥{total_remaining:,}\n"
        else:
            result += "尚未记录任何支出\n"
        
        result += f"创建时间: {budget['created_time']}\n\n"
    
    return result 