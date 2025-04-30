"""
虚拟酒店数据和预订管理
"""
from datetime import datetime, timedelta
import uuid

# 虚拟酒店数据库
HOTELS = [
    {
        "hotel_id": "SH001",
        "name": "上海外滩华尔道夫酒店",
        "city": "上海",
        "district": "黄浦区",
        "address": "黄浦区中山东一路2号",
        "stars": 5,
        "rating": 4.8,
        "amenities": ["游泳池", "健身中心", "Spa", "餐厅", "酒吧", "商务中心", "会议室"],
        "description": "位于上海外滩的豪华酒店，提供黄浦江和外滩美景，设施一流，服务卓越。",
        "image_url": "https://example.com/waldorf_shanghai.jpg",
        "price_range": "¥2,000-5,000"
    },
    {
        "hotel_id": "SH002",
        "name": "上海半岛酒店",
        "city": "上海",
        "district": "黄浦区",
        "address": "黄浦区中山东一路32号",
        "stars": 5,
        "rating": 4.9,
        "amenities": ["游泳池", "健身中心", "Spa", "餐厅", "酒吧", "商务中心", "会议室", "豪华轿车接送"],
        "description": "百年经典酒店品牌，位于外滩核心位置，拥有极致奢华的客房和世界级餐饮。",
        "image_url": "https://example.com/peninsula_shanghai.jpg",
        "price_range": "¥2,500-6,000"
    },
    {
        "hotel_id": "SH003",
        "name": "上海浦东香格里拉大酒店",
        "city": "上海",
        "district": "浦东新区",
        "address": "浦东新区富城路33号",
        "stars": 5,
        "rating": 4.7,
        "amenities": ["游泳池", "健身中心", "Spa", "餐厅", "酒吧", "商务中心"],
        "description": "位于浦东商务区的豪华酒店，靠近陆家嘴金融中心，提供优质服务和设施。",
        "image_url": "https://example.com/shangri_la_pudong.jpg",
        "price_range": "¥1,500-3,500"
    },
    {
        "hotel_id": "SH004",
        "name": "上海静安香格里拉大酒店",
        "city": "上海",
        "district": "静安区",
        "address": "静安区南京西路1218号",
        "stars": 5,
        "rating": 4.6,
        "amenities": ["游泳池", "健身中心", "Spa", "餐厅", "酒吧"],
        "description": "位于静安寺商圈的高档酒店，购物和用餐便利，环境舒适豪华。",
        "image_url": "https://example.com/shangri_la_jing_an.jpg",
        "price_range": "¥1,400-3,200"
    },
    {
        "hotel_id": "SH005",
        "name": "上海外滩悦榕庄",
        "city": "上海",
        "district": "黄浦区",
        "address": "黄浦区中山东一路558号",
        "stars": 5,
        "rating": 4.8,
        "amenities": ["游泳池", "健身中心", "Spa", "餐厅", "屋顶酒吧"],
        "description": "悦榕庄品牌的都市度假酒店，位于外滩，提供宽敞套房和高端Spa体验。",
        "image_url": "https://example.com/banyan_tree_shanghai.jpg",
        "price_range": "¥2,200-5,500"
    },
    {
        "hotel_id": "SH006",
        "name": "上海和平饭店",
        "city": "上海",
        "district": "黄浦区",
        "address": "黄浦区南京东路20号",
        "stars": 5,
        "rating": 4.5,
        "amenities": ["游泳池", "健身中心", "历史遗产之旅", "餐厅", "爵士酒吧"],
        "description": "上海历史名店，建于1929年，保留了经典的装潢风格，为宾客提供难忘的历史文化体验。",
        "image_url": "https://example.com/peace_hotel_shanghai.jpg",
        "price_range": "¥1,800-4,000"
    },
    {
        "hotel_id": "SH007",
        "name": "上海宝格丽酒店",
        "city": "上海",
        "district": "静安区",
        "address": "静安区北京西路33号",
        "stars": 5,
        "rating": 4.7,
        "amenities": ["游泳池", "健身中心", "Spa", "米其林星级餐厅", "酒吧"],
        "description": "奢侈品牌宝格丽打造的时尚精品酒店，设计感强，提供高品质餐饮体验。",
        "image_url": "https://example.com/bulgari_shanghai.jpg",
        "price_range": "¥2,800-6,500"
    },
    {
        "hotel_id": "SH008",
        "name": "上海浦东丽思卡尔顿酒店",
        "city": "上海",
        "district": "浦东新区",
        "address": "浦东新区世纪大道8号",
        "stars": 5,
        "rating": 4.6,
        "amenities": ["游泳池", "健身中心", "Spa", "餐厅", "行政酒廊"],
        "description": "位于上海国金中心的豪华酒店，拥有壮观的城市景观和精致的服务。",
        "image_url": "https://example.com/ritz_carlton_pudong.jpg",
        "price_range": "¥1,900-4,500"
    },
    {
        "hotel_id": "SH009",
        "name": "上海新天地朗廷酒店",
        "city": "上海",
        "district": "黄浦区",
        "address": "黄浦区马当路99号",
        "stars": 5,
        "rating": 4.5,
        "amenities": ["游泳池", "健身中心", "Spa", "中餐厅", "西餐厅"],
        "description": "位于充满历史文化的新天地区域，融合了中西文化的现代豪华酒店。",
        "image_url": "https://example.com/langham_xintiandi.jpg",
        "price_range": "¥1,500-3,800"
    },
    {
        "hotel_id": "SH010",
        "name": "上海安达仕酒店",
        "city": "上海",
        "district": "静安区",
        "address": "静安区石门一路88号",
        "stars": 5,
        "rating": 4.6,
        "amenities": ["屋顶游泳池", "健身中心", "Spa", "多家特色餐厅"],
        "description": "凯悦旗下的时尚生活方式酒店品牌，位于新兴的苏河湾地区，设计感十足。",
        "image_url": "https://example.com/andaz_shanghai.jpg",
        "price_range": "¥1,600-3,500"
    },
    {
        "hotel_id": "SH011",
        "name": "上海虹桥绿地铂骊酒店",
        "city": "上海",
        "district": "闵行区",
        "address": "闵行区虹桥路2277号",
        "stars": 4,
        "rating": 4.3,
        "amenities": ["健身中心", "餐厅", "商务中心", "会议室"],
        "description": "靠近虹桥交通枢纽的商务酒店，交通便利，设施齐全。",
        "image_url": "https://example.com/primus_hongqiao.jpg",
        "price_range": "¥800-1,500"
    },
    {
        "hotel_id": "SH012",
        "name": "上海南外滩W酒店",
        "city": "上海",
        "district": "黄浦区",
        "address": "黄浦区中山南路66号",
        "stars": 5,
        "rating": 4.5,
        "amenities": ["泳池", "健身中心", "特色餐厅", "酒吧", "Spa"],
        "description": "时尚潮流的W酒店品牌，位于南外滩，拥有现代设计和活力氛围。",
        "image_url": "https://example.com/w_shanghai.jpg",
        "price_range": "¥1,700-3,800"
    },
    {
        "hotel_id": "SH013",
        "name": "上海世茂皇家艾美酒店",
        "city": "上海",
        "district": "浦东新区",
        "address": "浦东新区世纪大道1288号",
        "stars": 5,
        "rating": 4.4,
        "amenities": ["室内游泳池", "健身中心", "Spa", "多家餐厅"],
        "description": "位于浦东世纪大道的豪华酒店，提供舒适客房和高品质服务。",
        "image_url": "https://example.com/le_royal_meridien.jpg",
        "price_range": "¥1,300-2,800"
    },
    {
        "hotel_id": "SH014",
        "name": "上海中心大厦J酒店",
        "city": "上海",
        "district": "浦东新区",
        "address": "浦东新区世纪大道100号",
        "stars": 5,
        "rating": 4.7,
        "amenities": ["世界最高酒店", "无边泳池", "高空观景台", "米其林餐厅"],
        "description": "位于上海中心大厦的超高层酒店，拥有世界顶级的景观和服务。",
        "image_url": "https://example.com/j_hotel_shanghai.jpg",
        "price_range": "¥2,500-8,000"
    },
    {
        "hotel_id": "SH015",
        "name": "上海嘉里大酒店",
        "city": "上海",
        "district": "浦东新区",
        "address": "浦东新区花木路1388号",
        "stars": 5,
        "rating": 4.5,
        "amenities": ["游泳池", "健身中心", "Spa", "多家餐厅", "购物中心直连"],
        "description": "与嘉里中心相连的豪华商务酒店，提供便捷的购物和餐饮体验。",
        "image_url": "https://example.com/kerry_hotel_pudong.jpg",
        "price_range": "¥1,200-2,600"
    },
    {
        "hotel_id": "SH016",
        "name": "上海中油阳光大酒店",
        "city": "上海",
        "district": "长宁区",
        "address": "长宁区仙霞路1525号",
        "stars": 4,
        "rating": 4.2,
        "amenities": ["游泳池", "健身中心", "餐厅", "会议设施"],
        "description": "位于长宁区的商务酒店，环境舒适，交通便利。",
        "image_url": "https://example.com/petrochina_hotel.jpg",
        "price_range": "¥700-1,400"
    },
    {
        "hotel_id": "SH017",
        "name": "上海兴荣温德姆酒店",
        "city": "上海",
        "district": "闵行区",
        "address": "闵行区沪闵路187号",
        "stars": 4,
        "rating": 4.1,
        "amenities": ["健身中心", "餐厅", "商务中心", "会议室"],
        "description": "适合商务旅行的实用型酒店，性价比高，服务周到。",
        "image_url": "https://example.com/wyndham_xingrong.jpg",
        "price_range": "¥600-1,200"
    },
    {
        "hotel_id": "SH018",
        "name": "上海雅居乐万豪酒店",
        "city": "上海",
        "district": "徐汇区",
        "address": "徐汇区漕宝路1888号",
        "stars": 5,
        "rating": 4.4,
        "amenities": ["游泳池", "健身中心", "Spa", "餐厅", "行政酒廊"],
        "description": "位于徐汇区的五星级酒店，靠近地铁站，交通便利。",
        "image_url": "https://example.com/marriott_agile.jpg",
        "price_range": "¥1,100-2,200"
    },
    {
        "hotel_id": "SH019",
        "name": "上海浦东喜来登由由酒店",
        "city": "上海",
        "district": "浦东新区",
        "address": "浦东新区浦建路38号",
        "stars": 5,
        "rating": 4.3,
        "amenities": ["游泳池", "健身中心", "餐厅", "酒吧"],
        "description": "位于浦东的老牌五星级酒店，提供稳定优质的服务和体验。",
        "image_url": "https://example.com/sheraton_pudong.jpg",
        "price_range": "¥900-1,800"
    },
    {
        "hotel_id": "SH020",
        "name": "上海七宝宝龙艾美酒店",
        "city": "上海",
        "district": "闵行区",
        "address": "闵行区漕宝路3555号",
        "stars": 5,
        "rating": 4.2,
        "amenities": ["游泳池", "健身中心", "Spa", "餐厅"],
        "description": "位于七宝古镇附近的现代豪华酒店，环境舒适，设施齐全。",
        "image_url": "https://example.com/le_meridien_qibao.jpg",
        "price_range": "¥800-1,700"
    }
]

# 定义房型数据
ROOM_TYPES = {
    "SH001": [  # 上海外滩华尔道夫酒店
        {
            "type_id": "SH001-DLX",
            "name": "豪华大床房",
            "bed_type": "1张特大床",
            "area": "50平方米",
            "view": "城市景观",
            "max_guests": 2,
            "breakfast": True,
            "cancellation": "入住前24小时可免费取消",
            "amenities": ["免费WiFi", "迷你吧", "咖啡机", "高清电视"],
            "price": 2200,
            "available": 8
        },
        {
            "type_id": "SH001-RVR",
            "name": "江景套房",
            "bed_type": "1张特大床",
            "area": "80平方米",
            "view": "黄浦江景观",
            "max_guests": 2,
            "breakfast": True,
            "cancellation": "入住前48小时可免费取消",
            "amenities": ["免费WiFi", "迷你吧", "咖啡机", "高清电视", "独立客厅", "管家服务"],
            "price": 4500,
            "available": 3
        },
        {
            "type_id": "SH001-TWN",
            "name": "豪华双床房",
            "bed_type": "2张单人床",
            "area": "50平方米",
            "view": "城市景观",
            "max_guests": 3,
            "breakfast": True,
            "cancellation": "入住前24小时可免费取消",
            "amenities": ["免费WiFi", "迷你吧", "咖啡机", "高清电视"],
            "price": 2200,
            "available": 5
        }
    ],
    "SH002": [  # 上海半岛酒店
        {
            "type_id": "SH002-DLX",
            "name": "豪华客房",
            "bed_type": "1张特大床",
            "area": "60平方米",
            "view": "花园景观",
            "max_guests": 2,
            "breakfast": True,
            "cancellation": "入住前24小时可免费取消",
            "amenities": ["免费WiFi", "迷你吧", "咖啡机", "高清电视", "平板电脑控制系统"],
            "price": 2800,
            "available": 6
        },
        {
            "type_id": "SH002-RVR",
            "name": "豪华江景客房",
            "bed_type": "1张特大床",
            "area": "60平方米",
            "view": "黄浦江景观",
            "max_guests": 2,
            "breakfast": True,
            "cancellation": "入住前48小时可免费取消",
            "amenities": ["免费WiFi", "迷你吧", "咖啡机", "高清电视", "平板电脑控制系统"],
            "price": 3500,
            "available": 4
        },
        {
            "type_id": "SH002-SUT",
            "name": "行政套房",
            "bed_type": "1张特大床",
            "area": "120平方米",
            "view": "黄浦江全景",
            "max_guests": 2,
            "breakfast": True,
            "cancellation": "入住前72小时可免费取消",
            "amenities": ["免费WiFi", "迷你吧", "咖啡机", "高清电视", "平板电脑控制系统", "专属管家服务", "免费机场接送"],
            "price": 5800,
            "available": 2
        }
    ],
    # 其他酒店的房型数据可以类似定义，这里省略
}

# 为其他酒店生成简化的房型数据
for hotel in HOTELS[2:]:
    hotel_id = hotel["hotel_id"]
    if hotel_id not in ROOM_TYPES:
        price_range = hotel["price_range"].replace("¥", "").split("-")
        min_price = int(price_range[0].replace(",", ""))
        
        ROOM_TYPES[hotel_id] = [
            {
                "type_id": f"{hotel_id}-DLX",
                "name": "豪华大床房",
                "bed_type": "1张特大床",
                "area": "45-55平方米",
                "view": "城市景观",
                "max_guests": 2,
                "breakfast": True,
                "cancellation": "入住前24小时可免费取消",
                "amenities": ["免费WiFi", "迷你吧", "高清电视"],
                "price": min_price,
                "available": 5
            },
            {
                "type_id": f"{hotel_id}-TWN",
                "name": "豪华双床房",
                "bed_type": "2张单人床",
                "area": "45-55平方米",
                "view": "城市景观",
                "max_guests": 3,
                "breakfast": True,
                "cancellation": "入住前24小时可免费取消",
                "amenities": ["免费WiFi", "迷你吧", "高清电视"],
                "price": min_price + 100,
                "available": 4
            },
            {
                "type_id": f"{hotel_id}-SUT",
                "name": "行政套房",
                "bed_type": "1张特大床",
                "area": "65-80平方米",
                "view": "城市景观或花园景观",
                "max_guests": 2,
                "breakfast": True,
                "cancellation": "入住前48小时可免费取消",
                "amenities": ["免费WiFi", "迷你吧", "咖啡机", "高清电视", "行政酒廊特权"],
                "price": min_price * 1.8,
                "available": 2
            }
        ]

# 酒店预订记录
BOOKINGS = {}

def book_hotel_room(hotel_id, room_type_id, guest_name, id_number, phone, check_in_date, check_out_date):
    """
    创建酒店预订记录
    
    参数:
    - hotel_id: 酒店ID
    - room_type_id: 房型ID
    - guest_name: 客人姓名
    - id_number: 身份证号
    - phone: 联系电话
    - check_in_date: 入住日期
    - check_out_date: 退房日期
    
    返回:
    - booking_id: 预订ID
    - 如果房间不可用或不存在，返回None
    """
    # 检查酒店是否存在
    hotel = None
    for h in HOTELS:
        if h["hotel_id"] == hotel_id:
            hotel = h
            break
    
    if hotel is None:
        return None
    
    # 检查房型是否存在
    room_type = None
    if hotel_id in ROOM_TYPES:
        for rt in ROOM_TYPES[hotel_id]:
            if rt["type_id"] == room_type_id:
                room_type = rt
                break
    
    if room_type is None:
        return None
    
    # 检查房间是否有空余
    if room_type["available"] <= 0:
        return None
    
    # 生成预订ID
    booking_id = f"B{uuid.uuid4().hex[:8].upper()}"
    
    # 创建预订记录
    booking = {
        "booking_id": booking_id,
        "hotel_id": hotel_id,
        "hotel_name": hotel["name"],
        "room_type_id": room_type_id,
        "room_type_name": room_type["name"],
        "guest_name": guest_name,
        "id_number": id_number,
        "phone": phone,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "price": room_type["price"],
        "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "已确认"
    }
    
    # 保存预订记录
    BOOKINGS[booking_id] = booking
    
    # 更新可用房间数量
    room_type["available"] -= 1
    
    return booking_id

def get_booking(booking_id):
    """
    获取预订记录
    
    参数:
    - booking_id: 预订ID
    
    返回:
    - 预订记录，如果不存在返回None
    """
    return BOOKINGS.get(booking_id) 