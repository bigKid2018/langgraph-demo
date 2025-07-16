from state import State
from utils.llm_manager import get_llm, get_llm_info


# 定义 chatbot 节点
def chatbot(state: State):
    """
    这是一个节点函数。它接收当前状态，调用 LLM，并返回要更新到状态中的内容。
    """
    llm = get_llm()
    llm_info = get_llm_info()

    print(f"---调用 CHATBOT 节点 ({llm_info['type']}: {llm_info['azure_deployment']})---")
    return {"messages": [llm.invoke(state["messages"])]}
