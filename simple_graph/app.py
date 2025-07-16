from langgraph.graph import StateGraph, END
from state import State
from chatbot import chatbot
from utils.llm_manager import get_llm_info


def create_graph():
    """创建并编译图"""
    # 初始化图构建器
    graph_builder = StateGraph(State)

    # 添加节点
    graph_builder.add_node("chatbot", chatbot)

    # 设置入口点
    graph_builder.set_entry_point("chatbot")

    # 添加边，将 chatbot 节点连接到终点
    graph_builder.add_edge("chatbot", END)

    # 编译图
    return graph_builder.compile()


def visualize_graph(graph):
    """可视化图形结构"""
    try:
        # 尝试生成 mermaid 图并保存到文件
        mermaid_code = graph.get_graph().draw_mermaid()
        with open('graph_visualization.mmd', 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        print("图形结构已保存到 graph_visualization.mmd 文件")
        print("可以使用 Mermaid 编辑器查看图形：https://mermaid.live/")
    except Exception as e:
        print(f"无法生成可视化图: {e}")
        print("跳过可视化步骤，继续运行聊天机器人。")


def run_chat():
    """运行聊天机器人"""
    graph = create_graph()

    # 显示LLM信息
    llm_info = get_llm_info()
    print(f"聊天机器人启动！使用 {llm_info['type']} 模式 ({llm_info['azure_deployment']})")
    if llm_info['is_mock']:
        print("⚠️ 当前使用模拟模式，设置 AZURE_OPENAI_API_KEY 环境变量可启用真实LLM")
    print("输入 'quit', 'exit' 或 'q' 退出。")
    print("=" * 50)

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        try:
            # 将用户输入封装成 LangChain 的消息格式
            for event in graph.stream({"messages": [("user", user_input)]}):
                # stream() 返回一个事件流，我们需要解析它来获取最新的消息
                for value in event.values():
                    # 打印助手的最新回复
                    print("Assistant:", value["messages"][-1].content)
        except Exception as e:
            print(f"错误: {e}")
            print("请检查 OpenAI API 密钥和网络连接。")


if __name__ == "__main__":
    # 创建图并可视化
    graph = create_graph()
    visualize_graph(graph)

    # 启动聊天
    run_chat()
