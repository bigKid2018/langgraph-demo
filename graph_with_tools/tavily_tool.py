from langchain_tavily import TavilySearch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_manager import get_llm

# 定义搜索工具
tavily_tool = TavilySearch(max_results=2)
tools = [tavily_tool]

# 将模型与工具绑定，这样模型就知道它有哪些工具可用
# 并能生成正确的 tool_calls
llm = get_llm()
model_with_tools = llm.bind_tools(tools)
