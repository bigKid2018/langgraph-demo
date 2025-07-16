# LangGraph Azure OpenAI 聊天机器人 Demo

这是一个基于 LangGraph 的 Azure OpenAI 聊天机器人示例，演示了如何构建和使用 LangGraph 应用程序，支持统一的 LLM 管理和配置系统。

## 📁 文件结构

```
demo1/
├── .env                # 环境变量配置文件
├── .gitignore          # Git忽略文件
├── app.py              # 主应用程序
├── chatbot.py          # 聊天机器人节点
├── config.py           # 配置管理模块
├── llm_manager.py      # 统一LLM管理器
├── README.md           # 本说明文档
├── requirement.txt     # 依赖项文件
└── state.py            # 状态定义
```

## 🔧 功能说明

### 核心模块
- **state.py**: 定义了 `State` 类型，包含消息列表和状态管理
- **chatbot.py**: 实现聊天机器人节点，处理用户消息并调用 LLM
- **app.py**: 主应用程序，创建图结构并管理聊天循环

### 配置系统
- **.env**: 环境变量配置文件，包含 Azure OpenAI API 密钥和配置参数
- **config.py**: 配置管理模块，统一管理所有环境变量和配置
- **llm_manager.py**: 统一的 LLM 管理器，支持 Azure OpenAI 和自动降级到模拟模式

## 🏗️ 图结构说明

### 当前图结构
```
Entry Point → chatbot → END
```

### 执行逻辑
1. **外部循环模式**：每次用户输入都是独立的图执行
2. **执行流程**：
   - 用户输入 → 启动新的图执行
   - 进入 `chatbot` 节点（入口点）
   - 处理用户消息，调用 Azure OpenAI
   - 通过普通边流向 `END` 节点
   - 图执行结束，返回结果
   - 回到 Python 的 `while` 循环，等待下一次输入

### 图结构特点
- **线性结构**：简单的单向流程
- **状态管理**：通过 `State` 对象维护对话历史
- **消息处理**：使用 LangChain 的消息格式
- **流式处理**：支持实时响应输出

## 🚀 运行方式

### 1. 环境准备
确保已安装 Python 3.8+ 和虚拟环境。

### 2. 安装依赖
```bash
pip install -r requirement.txt
```

### 3. 配置环境变量
编辑 `.env` 文件，设置你的 Azure OpenAI 配置：
```env
# Azure OpenAI 配置
AZURE_OPENAI_API_KEY="your-azure-api-key"
AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o"
AZURE_OPENAI_API_VERSION="2024-02-15-preview"

# LangChain 配置（可选）
LANGCHAIN_API_KEY="your-langchain-key"
LANGCHAIN_TRACING_V2="true"

# Tavily 配置（可选）
TAVILY_API_KEY="your-tavily-key"

# LLM 配置（可选）
LLM_TEMPERATURE="0"
LLM_MAX_TOKENS="2000"
```

### 4. 启动应用
```bash
cd demo1
python app.py
```

## 💻 使用示例

```
$ python app.py
📋 当前配置状态:
  azure_openai_api_key: 已设置
  azure_openai_endpoint: https://your-resource.openai.azure.com
  azure_deployment: gpt-4o
  azure_api_version: 2024-02-15-preview
  ...

🚀 正在初始化Azure OpenAI LLM: gpt-4o
✅ Azure OpenAI LLM已成功初始化: gpt-4o
聊天机器人启动！使用 azure_openai 模式 (gpt-4o)
输入 'quit', 'exit' 或 'q' 退出。
==================================================
User: 你好
---调用 CHATBOT 节点 (azure_openai: gpt-4o)---
Assistant: 你好！很高兴见到你。有什么我可以帮助你的吗？
User: q
Goodbye!
```

## 🎯 核心特性

### Azure OpenAI 支持
- ✅ 完整支持 Azure OpenAI 服务
- ✅ 自动配置管理和验证
- ✅ 支持多种部署模型
- ✅ API 版本管理

### 统一配置管理
- ✅ `.env` 文件统一管理敏感信息
- ✅ 类型安全的配置访问
- ✅ 环境变量和动态配置支持
- ✅ 配置状态实时监控

### 智能降级机制
- ✅ 无 API 密钥时自动切换到模拟模式
- ✅ 错误处理和用户友好提示
- ✅ 配置验证和状态检查

### LLM 管理
- ✅ 单例模式确保全局唯一实例
- ✅ 统一接口，所有模块共享
- ✅ 支持动态配置更新
- ✅ 实时状态监控

## 🔧 API 使用

### 获取 LLM 实例
```python
from llm_manager import get_llm, get_llm_info

# 获取 LLM 实例
llm = get_llm()

# 获取 LLM 信息
info = get_llm_info()
print(f"类型: {info['type']}")
print(f"部署: {info['azure_deployment']}")
```

### 配置管理
```python
from config import Config

# 打印配置状态
Config.print_config_status()

# 检查 API 密钥
if Config.is_api_key_set():
    print("API 密钥已设置")

# 获取 Azure OpenAI 配置
config = Config.get_azure_openai_config()
```

### 动态配置
```python
from llm_manager import configure_llm

# 动态更新配置
configure_llm(
    azure_deployment="gpt-35-turbo",
    temperature=0.7,
    max_tokens=1000
)
```

## 📊 依赖项

主要依赖项：
- `langgraph`: 图结构和工作流管理
- `langchain`: LLM 抽象和工具
- `langchain-openai`: Azure OpenAI 集成
- `python-dotenv`: 环境变量管理
- `tavily-python`: 搜索工具支持

## ⚠️ 注意事项

1. **API 密钥安全**: 
   - 永远不要将 `.env` 文件提交到版本控制
   - 使用 `.gitignore` 排除敏感文件

2. **配置验证**:
   - 启动前确保 Azure OpenAI 配置正确
   - 检查端点 URL 和部署名称

3. **网络连接**:
   - 确保能够访问 Azure OpenAI 端点
   - 检查防火墙和代理设置

4. **成本管理**:
   - 监控 Azure OpenAI 使用量
   - 合理设置 `max_tokens` 限制

## 🚀 扩展建议

### 图结构增强
- 添加条件边实现图内循环
- 支持多节点工作流
- 实现分支和合并逻辑
- 添加错误处理节点

### 功能扩展
- 支持多模态输入（图像、文档）
- 添加工具调用和函数执行
- 实现对话历史持久化
- 集成搜索和知识库

### 技术改进
- 支持更多 LLM 提供商
- 添加调用统计和监控
- 实现成本追踪和优化
- 支持批处理和并发

## 📝 更新日志

### v1.0.0 (最新)
- ✅ 完整的 Azure OpenAI 支持
- ✅ 统一配置管理系统
- ✅ 智能降级机制
- ✅ 单例 LLM 管理器
- ✅ 完善的错误处理

### 特性亮点
- 🎯 开箱即用的 Azure OpenAI 集成
- 🔧 灵活的配置系统
- 📊 实时状态监控
- 🔄 自动故障转移
- 🏗️ 清晰的图结构设计

---

**开始使用**: 配置 `.env` 文件并运行 `python app.py`  
**需要帮助?**: 检查配置状态和 Azure OpenAI 连接  
**想扩展?**: 参考扩展建议添加更多功能 