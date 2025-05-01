from typing import TypedDict, Optional, Dict, List
from langgraph.prebuilt import create_react_agent

class ToolCall(TypedDict):
    tool_name: str  # 工具名称
    tool_input: Dict  # 工具输入参数

class AgentResponse(TypedDict):
    thoughts: str  # 代理的推理过程
    action: Optional[ToolCall]  # 可选的工具调用
    answer: Optional[str]  # 可选的最终回答