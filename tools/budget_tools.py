"""
Travel budget management related tool functions
"""
from datetime import datetime
import uuid

# Data structures for storing user budgets and expenses
TRAVEL_BUDGETS = {}
EXPENSES = {}

def estimate_travel_budget(destination, days, traveler_count, travel_style="standard"):
    """
    Estimate travel total budget
    
    Parameters:
    - destination: Destination, such as "Shanghai", "Tokyo"
    - days: Number of travel days
    - traveler_count: Number of travelers
    - travel_style: Travel style, options include "economy", "standard", "luxury"
    
    Returns:
    - Budget estimation result, including total budget and detailed breakdown
    """
    # Base costs for different travel styles (per person per day)
    base_costs = {
        "economy": {"accommodation": 300, "dining": 150, "transportation": 100, "attractions": 100, "shopping": 200, "other": 50},
        "standard": {"accommodation": 600, "dining": 300, "transportation": 150, "attractions": 150, "shopping": 500, "other": 100},
        "luxury": {"accommodation": 1500, "dining": 600, "transportation": 300, "attractions": 300, "shopping": 1000, "other": 300}
    }
    
    # Adjustment factors for specific cities
    city_factors = {
        "Shanghai": 1.2, "Beijing": 1.1, "Guangzhou": 1.0, "Shenzhen": 1.1, "Hangzhou": 1.0,
        "Tokyo": 1.5, "Osaka": 1.3, "Kyoto": 1.3, "Seoul": 1.2, "Bangkok": 0.8,
        "Singapore": 1.4, "Hong Kong": 1.5, "New York": 1.8, "Paris": 1.6, "London": 1.7,
        "Rome": 1.5, "Sydney": 1.5, "Dubai": 1.6, "Maldives": 2.0
    }
    
    # Get city factor, default to 1.0 if not in the list
    city_factor = city_factors.get(destination, 1.0)
    
    # Get base costs
    base = base_costs.get(travel_style, base_costs["standard"])
    
    # Calculate budget for each category
    budget_items = {}
    total_budget = 0
    
    for category, daily_cost in base.items():
        # Apply city factor, number of travelers, and days
        category_cost = daily_cost * city_factor * traveler_count * days
        budget_items[category] = round(category_cost)
        total_budget += category_cost
    
    # Estimate round-trip flight costs (per person)
    flight_costs = {
        "domestic": {"economy": 1500, "standard": 2500, "luxury": 5000},
        "asia": {"economy": 3000, "standard": 5000, "luxury": 12000},
        "intercontinental": {"economy": 6000, "standard": 10000, "luxury": 25000}
    }
    
    # Determine region based on destination
    if destination in ["Shanghai", "Beijing", "Guangzhou", "Shenzhen", "Hangzhou"]:
        region = "domestic"
    elif destination in ["Tokyo", "Osaka", "Kyoto", "Seoul", "Bangkok", "Singapore", "Hong Kong"]:
        region = "asia"
    else:
        region = "intercontinental"
    
    # Add flight budget
    flight_budget = flight_costs[region][travel_style] * traveler_count
    budget_items["flights"] = flight_budget
    total_budget += flight_budget
    
    # Generate budget ID and save budget information
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
    
    # Format output
    result = f"Travel Budget Estimate (ID: {budget_id}):\n\n"
    result += f"Destination: {destination}\n"
    result += f"Travel Duration: {days} days\n"
    result += f"Number of Travelers: {traveler_count}\n"
    result += f"Travel Style: {travel_style}\n\n"
    
    result += "Budget Breakdown:\n"
    for category, amount in budget_items.items():
        result += f"- {category}: ¥{amount:,}\n"
    
    result += f"\nTotal Budget: ¥{round(total_budget):,}\n"
    result += f"Budget per Person: ¥{round(total_budget/traveler_count):,}\n"
    result += f"Budget per Person per Day: ¥{round(total_budget/traveler_count/days):,}\n"
    
    return result

def track_expense(budget_id, category, amount, description=None):
    """
    Record travel expense
    
    Parameters:
    - budget_id: Budget ID
    - category: Expense category, such as "accommodation", "dining", "transportation", etc.
    - amount: Expense amount
    - description: Expense description (optional)
    
    Returns:
    - Expense record confirmation and remaining budget information
    """
    # Check if budget ID exists
    if budget_id not in TRAVEL_BUDGETS:
        return "Cannot find this budget ID, please verify and try again."
    
    budget = TRAVEL_BUDGETS[budget_id]
    
    # Check if category is valid
    valid_categories = list(budget["budget_items"].keys())
    if category not in valid_categories:
        return f"Invalid expense category. Please use one of the following: {', '.join(valid_categories)}"
    
    # Generate expense ID
    expense_id = f"E{uuid.uuid4().hex[:8].upper()}"
    
    # Record expense
    if budget_id not in EXPENSES:
        EXPENSES[budget_id] = []
    
    EXPENSES[budget_id].append({
        "expense_id": expense_id,
        "category": category,
        "amount": amount,
        "description": description,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Calculate category spent and remaining budget
    category_budget = budget["budget_items"][category]
    category_spent = sum(e["amount"] for e in EXPENSES[budget_id] if e["category"] == category)
    category_remaining = category_budget - category_spent
    
    # Calculate total spent and remaining budget
    total_budget = budget["total_budget"]
    total_spent = sum(e["amount"] for e in EXPENSES[budget_id])
    total_remaining = total_budget - total_spent
    
    # Format output
    result = "Expense recorded!\n\n"
    result += f"Expense ID: {expense_id}\n"
    result += f"Category: {category}\n"
    result += f"Amount: ¥{amount:,}\n"
    
    if description:
        result += f"Description: {description}\n"
    
    result += f"\n{category} Category Budget: ¥{category_budget:,}\n"
    result += f"{category} Category Spent: ¥{category_spent:,}\n"
    result += f"{category} Category Remaining: ¥{category_remaining:,} "
    
    # Add budget usage percentage
    category_percent = (category_spent / category_budget) * 100
    result += f"({category_percent:.1f}% used)\n\n"
    
    result += f"Total Budget: ¥{total_budget:,}\n"
    result += f"Total Spent: ¥{total_spent:,}\n"
    result += f"Remaining Budget: ¥{total_remaining:,} "
    
    # Add total budget usage percentage
    total_percent = (total_spent / total_budget) * 100
    result += f"({total_percent:.1f}% used)"
    
    return result

def analyze_budget(budget_id):
    """
    Analyze budget usage
    
    Parameters:
    - budget_id: Budget ID
    
    Returns:
    - Budget usage analysis report
    """
    # Check if budget ID exists
    if budget_id not in TRAVEL_BUDGETS:
        return "Cannot find this budget ID, please verify and try again."
    
    budget = TRAVEL_BUDGETS[budget_id]
    
    # Check if there are expense records
    if budget_id not in EXPENSES or not EXPENSES[budget_id]:
        return f"No expenses recorded yet. Total budget: ¥{budget['total_budget']:,}"
    
    # Calculate total spent
    total_spent = sum(e["amount"] for e in EXPENSES[budget_id])
    remaining_budget = budget["total_budget"] - total_spent
    
    # Calculate percentage used
    percent_used = (total_spent / budget["total_budget"]) * 100
    
    # Calculate category breakdown
    category_data = {}
    for category, budget_amount in budget["budget_items"].items():
        category_spent = sum(e["amount"] for e in EXPENSES[budget_id] if e["category"] == category)
        category_remaining = budget_amount - category_spent
        
        if budget_amount > 0:
            category_percent = (category_spent / budget_amount) * 100
        else:
            category_percent = 0
        
        category_data[category] = {
            "budget": budget_amount,
            "spent": category_spent,
            "remaining": category_remaining,
            "percent": category_percent
        }
    
    # Sort categories by percentage used
    sorted_categories = sorted(category_data.items(), key=lambda x: x[1]["percent"], reverse=True)
    
    # Format output
    result = f"Budget Analysis (ID: {budget_id}):\n\n"
    result += f"Destination: {budget['destination']}\n"
    result += f"Travel Duration: {budget['days']} days\n"
    result += f"Number of Travelers: {budget['traveler_count']}\n"
    result += f"Travel Style: {budget['travel_style']}\n\n"
    
    result += f"Total Budget: ¥{budget['total_budget']:,}\n"
    result += f"Total Spent: ¥{total_spent:,} ({percent_used:.1f}% of total budget)\n"
    result += f"Remaining Budget: ¥{remaining_budget:,}\n\n"
    
    result += "Category Breakdown:\n"
    for category, data in sorted_categories:
        result += f"- {category}:\n"
        result += f"  Budget: ¥{data['budget']:,}\n"
        result += f"  Spent: ¥{data['spent']:,} ({data['percent']:.1f}%)\n"
        result += f"  Remaining: ¥{data['remaining']:,}\n"
    
    # Add expense list
    result += "\nExpense History:\n"
    sorted_expenses = sorted(EXPENSES[budget_id], key=lambda x: x["time"], reverse=True)
    for expense in sorted_expenses:
        result += f"- {expense['time']}: {expense['category']} - ¥{expense['amount']:,}"
        if expense["description"]:
            result += f" ({expense['description']})"
        result += "\n"
    
    return result

def compare_options(option_type, options):
    """
    Compare the cost and value of different options
    
    Parameters:
    - option_type: Type of option, such as "hotel", "transportation", etc.
    - options: List of options, format is [{"name":"Option1","cost":1000,"features":["Feature1","Feature2"]},...]
    
    Returns:
    - Comparison analysis result
    """
    if not options or len(options) < 2:
        return "At least two options are needed for comparison."
    
    # Calculate feature score for each option
    for option in options:
        option["feature_count"] = len(option.get("features", []))
        
        # Calculate value score (features per cost unit)
        if option["cost"] > 0:
            option["value_score"] = option["feature_count"] * 1000 / option["cost"]
        else:
            option["value_score"] = 0
    
    # Sort options by different criteria
    by_cost = sorted(options, key=lambda x: x["cost"])
    by_features = sorted(options, key=lambda x: x["feature_count"], reverse=True)
    by_value = sorted(options, key=lambda x: x["value_score"], reverse=True)
    
    # Format output
    result = f"Comparison of {option_type} Options:\n\n"
    
    # List all options with details
    result += "All Options:\n"
    for i, option in enumerate(options, 1):
        result += f"{i}. {option['name']}\n"
        result += f"   Cost: ¥{option['cost']:,}\n"
        result += f"   Features ({option['feature_count']}): {', '.join(option.get('features', []))}\n"
        result += f"   Value Score: {option['value_score']:.2f}\n\n"
    
    # Best options by different criteria
    result += "Best Options by Different Criteria:\n"
    result += f"- Most Economical: {by_cost[0]['name']} (¥{by_cost[0]['cost']:,})\n"
    result += f"- Most Features: {by_features[0]['name']} ({by_features[0]['feature_count']} features)\n"
    result += f"- Best Value: {by_value[0]['name']} (Score: {by_value[0]['value_score']:.2f})\n\n"
    
    # Comparison conclusion
    result += "Analysis:\n"
    
    # Price range
    price_min = by_cost[0]["cost"]
    price_max = by_cost[-1]["cost"]
    price_diff = price_max - price_min
    
    if price_min == price_max:
        result += "- All options have the same price.\n"
    else:
        result += f"- Price range: ¥{price_min:,} to ¥{price_max:,} (difference of ¥{price_diff:,}).\n"
    
    # Feature comparison
    feature_min = min(opt["feature_count"] for opt in options)
    feature_max = max(opt["feature_count"] for opt in options)
    if feature_min == feature_max:
        result += "- All options have the same number of features.\n"
    else:
        result += f"- Feature range: {feature_min} to {feature_max} features.\n"
    
    # Recommendation
    result += "\nRecommendation:\n"
    
    if by_value[0]["value_score"] > 1.5 * by_value[-1]["value_score"]:
        result += f"- The best value option is {by_value[0]['name']}, which offers significantly better value than others.\n"
    elif by_cost[0]["cost"] < 0.7 * by_cost[-1]["cost"] and by_cost[0]["feature_count"] >= 0.8 * by_features[0]["feature_count"]:
        result += f"- Consider the economical option {by_cost[0]['name']}, which offers good features at a lower price.\n"
    elif by_features[0]["feature_count"] > 1.5 * by_features[-1]["feature_count"] and by_features[0]["cost"] <= 1.3 * by_cost[0]["cost"]:
        result += f"- Consider the feature-rich option {by_features[0]['name']}, which offers many more features for a reasonable price increase.\n"
    else:
        result += f"- All options offer reasonable value. Choose based on your specific requirements and budget constraints.\n"
    
    return result

def get_budget_summary(budget_id=None):
    """
    Get budget summary information
    
    Parameters:
    - budget_id: Budget ID (optional), returns all budget summaries if not provided
    
    Returns:
    - Budget summary information
    """
    # If budget_id is provided, return details for that specific budget
    if budget_id:
        if budget_id not in TRAVEL_BUDGETS:
            return "Budget ID not found."
        
        budget = TRAVEL_BUDGETS[budget_id]
        
        # Calculate spent amounts
        total_spent = 0
        category_spent = {}
        
        if budget_id in EXPENSES:
            total_spent = sum(e["amount"] for e in EXPENSES[budget_id])
            
            for category in budget["budget_items"].keys():
                category_spent[category] = sum(e["amount"] for e in EXPENSES[budget_id] if e["category"] == category)
        
        # Calculate remaining budget
        remaining = budget["total_budget"] - total_spent
        
        # Format output
        result = f"Budget Summary (ID: {budget_id}):\n\n"
        result += f"Destination: {budget['destination']}\n"
        result += f"Travel Duration: {budget['days']} days\n"
        result += f"Number of Travelers: {budget['traveler_count']}\n"
        result += f"Travel Style: {budget['travel_style']}\n"
        result += f"Created: {budget['created_time']}\n\n"
        
        result += f"Total Budget: ¥{budget['total_budget']:,}\n"
        result += f"Total Spent: ¥{total_spent:,}\n"
        result += f"Remaining: ¥{remaining:,}\n\n"
        
        if total_spent > 0:
            percent_used = (total_spent / budget["total_budget"]) * 100
            result += f"Budget Usage: {percent_used:.1f}% used\n\n"
            
            result += "Category Breakdown:\n"
            for category, budget_amount in budget["budget_items"].items():
                spent = category_spent.get(category, 0)
                remaining_category = budget_amount - spent
                
                if budget_amount > 0:
                    percent = (spent / budget_amount) * 100
                    result += f"- {category}: ¥{spent:,} of ¥{budget_amount:,} ({percent:.1f}% used, ¥{remaining_category:,} remaining)\n"
                else:
                    result += f"- {category}: ¥{spent:,} of ¥{budget_amount:,}\n"
        
        return result
        
    # If no budget_id provided, return summary of all budgets
    else:
        if not TRAVEL_BUDGETS:
            return "No budgets found."
        
        result = "All Budget Summaries:\n\n"
        
        for bid, budget in TRAVEL_BUDGETS.items():
            # Calculate total spent
            total_spent = 0
            if bid in EXPENSES:
                total_spent = sum(e["amount"] for e in EXPENSES[bid])
            
            # Calculate remaining budget
            remaining = budget["total_budget"] - total_spent
            
            # Calculate percentage used
            if budget["total_budget"] > 0:
                percent_used = (total_spent / budget["total_budget"]) * 100
            else:
                percent_used = 0
            
            # Add to result
            result += f"{bid}: {budget['destination']} ({budget['days']} days, {budget['traveler_count']} travelers)\n"
            result += f"  Total: ¥{budget['total_budget']:,}, Spent: ¥{total_spent:,}, Remaining: ¥{remaining:,} ({percent_used:.1f}% used)\n"
            result += f"  Created: {budget['created_time']}\n\n"
        
        return result 