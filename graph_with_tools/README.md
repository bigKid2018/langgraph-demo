# Graph with Tools - 智能对话代理

这是一个基于 LangGraph 构建的智能对话代理，能够使用 Tavily 搜索工具来回答用户问题。该代理采用状态图的方式管理对话流程，支持工具调用和条件路由。

## 功能特性

- 🤖 **智能对话**: 基于 Azure OpenAI 的智能对话功能
- 🔍 **网络搜索**: 集成 Tavily 搜索工具，获取实时信息
- 📊 **状态管理**: 使用 LangGraph 管理对话状态和流程
- 🛠️ **工具调用**: 支持动态工具调用和结果处理
- 🔄 **条件路由**: 智能判断是否需要调用工具或结束对话
- 💾 **状态持久化**: 支持使用 SQLite 进行状态持久化存储
- 🎯 **模拟模式**: 支持无需真实 API 的模拟模式用于测试
- 📈 **可视化支持**: 支持图结构可视化（需要 IPython 环境）

## 项目结构

```
graph_with_tools/
├── graph.py          # 主要的图构建和执行逻辑
├── state.py          # 状态定义
├── tavily_tool.py    # Tavily 搜索工具配置
└── README.md         # 项目文档
```

## 核心组件

### 1. 状态管理 (`state.py`)
定义了对话状态结构，包含消息列表：
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
```

### 2. 工具配置 (`tavily_tool.py`)
配置 Tavily 搜索工具：
- 使用最新的 `langchain-tavily` 包
- 最多返回 2 个搜索结果
- 自动绑定到 LLM 模型

### 3. 图构建 (`graph.py`)
包含三个主要节点：
- **Agent 节点**: 调用 LLM 生成回答或工具调用请求
- **Tool 节点**: 执行工具调用并返回结果
- **条件路由**: 判断是否需要继续调用工具

**图的执行流程：**
1. 用户消息进入 Agent 节点
2. Agent 决定是否需要调用工具
3. 如果需要工具，路由到 Tool 节点执行
4. 工具执行完成后，返回 Agent 节点处理结果
5. Agent 生成最终回答或继续工具调用循环

## 环境配置

### 1. 依赖安装
```bash
pip install -r ../requirement.txt
```

**主要依赖包括：**
- `langgraph` - 状态图构建框架
- `langchain` - LLM 应用框架
- `langchain-openai` - OpenAI 集成
- `langchain-tavily` - Tavily 搜索工具集成
- `langgraph-checkpoint-sqlite` - 状态持久化支持
- `tavily-python` - Tavily Python SDK
- `python-dotenv` - 环境变量管理
- `IPython` - 交互式显示支持

### 2. 环境变量配置
创建 `.env` 文件并配置以下变量：

```bash
# Azure OpenAI 配置
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Tavily 搜索配置
TAVILY_API_KEY=your_tavily_api_key

# LangChain 配置（可选）
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_TRACING_V2=true

# LLM 参数配置
LLM_TEMPERATURE=0
LLM_MAX_TOKENS=2000
```

### 3. 获取 API 密钥

#### Azure OpenAI
1. 访问 [Azure Portal](https://portal.azure.com)
2. 创建 Azure OpenAI 资源
3. 获取 API 密钥和端点

#### Tavily API
1. 访问 [Tavily](https://tavily.com)
2. 注册账户并获取 API 密钥

## 使用方法

### 1. 直接运行
```bash
cd graph_with_tools
python graph.py
```

### 2. 编程调用
```python
from graph import create_graph

# 创建图
agent_graph = create_graph()

# 运行对话
user_query = "LangGraph 和 LangChain 有什么区别？"
for event in agent_graph.stream({"messages": [("user", user_query)]}):
    for node, value in event.items():
        print(f"--- 输出自节点: {node} ---")
        print(value["messages"][-1])
```

### 3. 批量处理
```python
from graph import create_graph

# 创建图
agent_graph = create_graph()

# 批量处理多个问题
questions = [
    "什么是 LangGraph？",
    "如何使用 Tavily 搜索？",
    "LangGraph 的优势是什么？"
]

for question in questions:
    print(f"\n问题: {question}")
    print("=" * 50)
    
    for event in agent_graph.stream({"messages": [("user", question)]}):
        for node, value in event.items():
            print(f"--- 输出自节点: {node} ---")
            print(value["messages"][-1])
```

### 4. 自定义配置
```python
from utils.llm_manager import configure_llm

# 动态配置 LLM 参数
configure_llm(
    temperature=0.7,
    max_tokens=1000
)
```

### 5. 图可视化
```python
from graph import create_graph

# 创建图
agent_graph = create_graph()

# 在 Jupyter 环境中显示图结构
try:
    from IPython.display import Image, display
    display(Image(agent_graph.get_graph().draw_mermaid_png()))
except ImportError:
    print("需要 IPython 环境来显示图形")
    # 或者输出 Mermaid 格式的图定义
    print(agent_graph.get_graph().draw_mermaid())
```

## 工作流程

1. **用户输入**: 用户提出问题
2. **Agent 处理**: LLM 分析问题，决定是否需要搜索
3. **工具调用**: 如果需要，调用 Tavily 搜索获取信息
4. **结果处理**: 处理搜索结果并生成回答
5. **输出回答**: 返回最终答案给用户

## 示例对话

```
用户: LangGraph 和 LangChain 有什么区别？

Agent: 我来为您搜索关于 LangGraph 和 LangChain 的最新信息...

[调用 Tavily 搜索工具]

Agent: 根据搜索结果，LangGraph 和 LangChain 的主要区别如下：

1. **定位不同**：
   - LangChain: 是一个用于构建 LLM 应用的框架
   - LangGraph: 是 LangChain 的扩展，专注于构建状态图和工作流

2. **应用场景**：
   - LangChain: 适合简单的链式处理
   - LangGraph: 适合复杂的多步骤、条件分支的应用

3. **状态管理**：
   - LangChain: 相对简单的状态传递
   - LangGraph: 提供更强大的状态管理和持久化
```

## 性能优化和最佳实践

### 1. 配置优化
- **温度设置**: 对于事实性查询，建议设置较低的温度 (0-0.3)
- **Token 限制**: 根据需要调整 `max_tokens` 参数，避免过长的响应
- **搜索结果数量**: Tavily 搜索默认返回 2 个结果，可根据需要调整

### 2. 错误处理
- 代码自动处理 API 调用失败的情况
- 支持降级到模拟模式用于测试
- 提供详细的日志输出便于调试

### 3. 扩展建议
- 可以添加更多工具（如计算器、数据库查询等）
- 支持自定义工具实现
- 可以集成状态持久化功能

## 故障排除

### 1. 导入错误
如果遇到 `IPython.display` 导入错误，代码会自动降级到文本模式。

### 2. API 密钥问题
- 检查 `.env` 文件是否正确配置
- 确认 API 密钥有效且有足够的配额
- 系统会自动切换到模拟模式如果 API 不可用

### 3. 网络问题
- 确保网络连接正常
- 检查防火墙设置
- 可能需要配置代理

### 4. 依赖问题
- 确保所有依赖包都已正确安装
- 如果遇到版本冲突，可以尝试创建虚拟环境
- 使用 `pip install -r requirement.txt` 确保依赖一致性

## 技术栈

- **LangGraph**: 状态图和工作流管理
- **LangChain**: LLM 应用框架
- **Azure OpenAI**: 大语言模型服务
- **Tavily**: 网络搜索 API
- **SQLite**: 状态持久化存储
- **Python**: 编程语言
- **IPython**: 交互式环境和可视化支持

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更多信息

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangChain 官方文档](https://python.langchain.com/)
- [Tavily API 文档](https://docs.tavily.com/)
- [Azure OpenAI 文档](https://learn.microsoft.com/zh-cn/azure/cognitive-services/openai/)

## 更新日志

### 最新版本特性
- ✅ 集成 Tavily 搜索工具
- ✅ 支持 Azure OpenAI 模型
- ✅ 状态持久化功能
- ✅ 图可视化支持
- ✅ 完整的错误处理机制
- ✅ 模拟模式支持
- ✅ 详细的文档和示例

### 计划中的功能
- 🔄 多轮对话记忆功能
- 🔄 更多工具集成
- 🔄 Web 界面支持
- 🔄 批量处理优化