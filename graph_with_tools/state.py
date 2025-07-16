from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


# 定义状态对象
# messages 键将存储对话消息列表。
# Annotated[list, add_messages] 的作用是让新的消息追加到列表中，而不是覆盖。
class State(TypedDict):
    messages: Annotated[list, add_messages]
