# 旅行助手系统

> [English Version](./README.md)

## 概述

旅行助手系统是一个智能多智能体旅行规划平台，帮助用户规划行程、搜索航班和酒店、管理预算，并创建全面的旅行行程单。该系统利用先进的语言模型和多智能体架构，提供个性化的旅行推荐和服务。

## 功能特点

- **智能行程规划**：根据用户偏好生成定制旅行计划
- **航班预订**：搜索和预订航班，提供详细信息
- **酒店预订**：根据位置、设施和预算查找并预订合适的酒店
- **预算管理**：估算、跟踪和分析旅行支出
- **交互式界面**：使用自然语言对话完成所有旅行规划需求
- **记忆管理**：在整个规划过程中保持对话上下文
- **实时信息**：集成搜索功能获取最新旅行信息
- **地图服务**：通过高德地图MCP服务访问位置和路线规划

## 技术栈

- **编程语言**：Python 3.11+
- **框架**：
  - LangGraph (用于智能体编排)
  - LangGraph Swarm (用于多智能体协作)
  - LangChain (用于LLM交互)
- **模型**：DeepSeek Chat API
- **内存管理**：LangGraph Memory Store和Checkpointer
- **外部服务**：
  - Tavily API (实时信息搜索)
  - 高德地图API (位置和地图服务)
- **数据**：用于开发和测试的模拟旅行数据

## 系统架构

系统围绕多智能体架构构建，包含专业化的智能体：

- **旅行日程智能体**：协调整体行程规划过程，集成了Tavily搜索获取实时旅行信息和高德地图MCP服务获取位置数据与路线规划
- **航班智能体**：管理航班搜索和预订操作
- **酒店智能体**：处理酒店搜索和预订服务
- **预算智能体**：提供财务规划和支出跟踪

这些智能体使用LangGraph Swarm框架进行通信和协作，实现高效的任务委派和信息共享。

## 项目结构

```
travel_agent/
│
├── main_groupchat.py     # 主入口点（群聊实现）
│
├── agents/               # 智能体定义
│   ├── travel_schedule_agent.py # 旅行规划协调器，集成地图服务
│   ├── flight_agent.py   # 航班搜索和预订智能体
│   ├── hotel_agent.py    # 酒店搜索和预订智能体
│   └── budget_agent.py   # 预算管理智能体
│
├── tools/                # 工具实现
│   ├── transfer_tool.py  # 智能体间转换工具
│   ├── flight_tools.py   # 航班相关工具
│   ├── hotel_tools.py    # 酒店相关工具
│   └── budget_tools.py   # 预算管理工具
│
├── data/                 # 数据文件
│   ├── flight_data.py    # 航班数据库
│   └── hotel_data.py     # 酒店数据库
│
└── requirements.txt      # Python依赖
```

## 安装指南

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/travel_agent.git
   cd travel_agent
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows系统: .venv\Scripts\activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 设置环境变量：
   ```bash
   # 创建包含API密钥的.env文件
   echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
   echo "TAVILY_API_KEY=your_tavily_api_key_here" >> .env
   echo "AMAP_API_KEY=your_amap_api_key_here" >> .env
   ```

## 使用方法

运行主应用程序：

```bash
python main_groupchat.py
```

系统将启动一个交互式会话，您可以用自然语言输入旅行查询。查询示例包括：

- "我想为2人规划一次5天的东京之行。"
- "查找5月15日从北京到上海的航班。"
- "显示上海有游泳池的酒店。"
- "你能帮我估算一下7天巴黎之行的预算吗？"
- "北京有哪些主要景点？"
- "在上海，从机场到市中心怎么走？"

## 会话示例

```
🌍 旅行助手已启动! 输入您的旅行问题，或输入 'exit' 退出。
📝 会话ID: 3f7b9a1c-8d24-4e61-9d7b-2a6fc98a5c7f

🧑‍💻 您: 我想下个月规划一次3天的上海之行。你能帮我安排航班和酒店吗？

🤖 助手: 我很乐意帮您规划3天的上海之行！

让我先为您找一些航班选项。请告诉我：
1. 您将从哪里出发？
2. 您的首选旅行日期是什么时候？
3. 将有多少人一起旅行？

一旦我有了这些信息，我就可以搜索航班，然后为您的上海之行找到合适的酒店。
```

## 未来计划

- 与真实旅行API集成获取实时数据
- 移动应用程序界面
- 多语言支持
- 行程共享和协作功能
- 自动行程优化

## 许可证

该项目采用MIT许可证 - 详情请参阅LICENSE文件。

## 联系方式

如有问题或反馈，请联系：[1302278835@qq.com](mailto:1302278835@qq.com) 