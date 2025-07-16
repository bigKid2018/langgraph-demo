import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import ToolMessage
from state import State
from tavily_tool import model_with_tools, tools
from langgraph.graph import StateGraph, END

try:
    from IPython.display import Image, display
except ImportError:
    Image = display = None


# Agent 节点
def agent(state: State):
    """
    调用绑定了工具的 LLM，LLM 的输出可能是直接回答，也可能包含工具调用请求。
    """
    print("---调用 AGENT 节点---")
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    # response 本身就是一个 AIMessage，可能包含 tool_calls
    return {"messages": [response]}


# 条件路由函数
def should_continue(state: State) -> str:
    """
    决定是继续调用工具还是结束。
    """
    print("---条件判断---")
    last_message = state["messages"][-1]
    # 如果最后一条消息中没有 tool_calls，则结束
    if not last_message.tool_calls:
        print("-> 决定结束")
        return "end"
    # 否则，继续执行工具
    else:
        print("-> 决定继续调用工具")
        return "continue"


# 工具执行节点
# 我们需要一个通用的工具执行节点，它能处理任何工具调用
def call_tool(state: State):
    """
    执行工具调用。
    """
    print("---调用工具节点---")
    last_message = state["messages"][-1]
    # 遍历所有工具调用请求
    tool_invocations = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        # 找到对应的工具
        tool_to_call = {t.name: t for t in tools}[tool_name]
        # 调用工具
        observation = tool_to_call.invoke(tool_call["args"])
        # 将结果封装成 ToolMessage
        tool_invocations.append(
            ToolMessage(content=str(observation), tool_call_id=tool_call["id"])
        )
    # 将工具执行结果添加到消息列表中
    return {"messages": tool_invocations}


def create_graph(checkpointer=None):
    # 重新初始化图构建器
    agent_graph_builder = StateGraph(State)

    # 添加新的节点
    agent_graph_builder.add_node("agent", agent)
    agent_graph_builder.add_node("action", call_tool)

    # 设置入口点
    agent_graph_builder.set_entry_point("agent")

    # 添加条件边
    agent_graph_builder.add_conditional_edges(
        "agent",  # 起始节点
        should_continue,  # 条件判断函数
        {
            "continue": "action",  # 如果返回 "continue"，则流向 "action" 节点
            "end": END  # 如果返回 "end"，则结束
        }
    )

    # 添加从工具节点回到 Agent 节点的普通边
    agent_graph_builder.add_edge("action", "agent")

    # 编译新的 Agent 图
    agent_graph = agent_graph_builder.compile(checkpointer=checkpointer)
    return agent_graph


def run_chat(agent_graph):
    # 可视化新的 Agent 图
    try:
        if Image and display:
            display(Image(agent_graph.get_graph().draw_mermaid_png()))
        else:
            print("无法生成可视化图。(IPython 未安装)")
    except Exception:
        print("无法生成可视化图。")

    # 运行 Agent
    user_query = "LangGraph 和 LangChain 有什么区别？用中文回答。"
    # 使用 stream 方法来观察每一步的状态变化
    for event in agent_graph.stream({"messages": [("user", user_query)]}):
        for node, value in event.items():
            print(f"--- 输出自节点: {node} ---")
            # 打印该节点处理后的消息列表中的最新消息
            print(value["messages"][-1])
        print("\n")


if __name__ == "__main__":
    # agent_graph = create_graph()
    # run_chat(agent_graph)
    
    from langgraph.checkpoint.sqlite import SqliteSaver

    # 使用 SQLite 作为持久化后端
    with SqliteSaver.from_conn_string(":memory:") as memory:  # :memory: 表示内存数据库，可替换为文件路径
        # 创建带有检查点的图
        agent_with_memory = create_graph(checkpointer=memory)

        # 调用时需要提供一个唯一的线程 ID (thread_id) 来区分不同的对话
        config = {"configurable": {"thread_id": "my-thread-1"}}
        
        # 第一次调用
        print("第一次调用：")
        response1 = agent_with_memory.invoke({"messages": [("user", "我的名字是张三")]}, config)
        print(response1['messages'][-1].content)
        
        # 第二次调用，Agent 会记得之前的对话
        print("\n第二次调用：")
        response2 = agent_with_memory.invoke({"messages": [("user", "我叫什么名字？")]}, config)
        print(response2['messages'][-1].content)  # 输出: 你的名字是张三。

