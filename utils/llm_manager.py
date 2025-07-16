import os
from typing import Optional, Dict, Any
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage
from utils.config import Config


class LLMManager:
    """LLM管理器 - 统一的 LLM 初始化和配置管理"""

    _instance = None
    _llm = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._llm is None:
            self._initialize_llm()

    def _initialize_llm(self):
        """初始化 LLM 实例"""
        # 打印配置状态
        Config.print_config_status()

        # 检查API密钥
        if not Config.is_api_key_set():
            print("❌ 未找到 AZURE_OPENAI_API_KEY 环境变量")
            print("🔄 切换到模拟模式...")
            self._llm = MockLLM()
            self._llm_type = "mock"
            return

        try:
            # 获取 Azure OpenAI 配置
            llm_config = Config.get_azure_openai_config()

            print(f"🚀 正在初始化Azure OpenAI LLM: {llm_config['azure_deployment']}")
            self._llm = AzureChatOpenAI(**llm_config)
            self._llm_type = "azure_openai"
            print(f"✅ Azure OpenAI LLM已成功初始化: {llm_config['azure_deployment']}")
        except Exception as e:
            print(f"⚠️ 无法初始化Azure OpenAI LLM: {e}")
            print("🔄 切换到模拟模式...")
            self._llm = MockLLM()
            self._llm_type = "mock"

    def get_llm(self):
        """获取 LLM 实例"""
        return self._llm

    def get_llm_type(self):
        """获取当前使用的 LLM 类型"""
        return self._llm_type

    def is_mock(self):
        """判断是否使用模拟模式"""
        return self._llm_type == "mock"


class MockLLM:
    """模拟 LLM - 用于测试和开发"""

    def __init__(self):
        self.model = "mock-gpt"
        self.temperature = 0

    def invoke(self, messages):
        """模拟 LLM 调用"""
        # 获取最后一条消息
        if not messages:
            return AIMessage(content="Hello! How can I help you?")

        last_message = messages[-1]
        if isinstance(last_message, tuple):
            user_content = last_message[1]
        elif hasattr(last_message, 'content'):
            user_content = last_message.content
        else:
            user_content = str(last_message)

        # 简单的回复逻辑
        user_content_lower = user_content.lower()

        if "hello" in user_content_lower or "hi" in user_content_lower:
            return AIMessage(content="Hello! How can I help you today?")
        elif "bye" in user_content_lower or "goodbye" in user_content_lower:
            return AIMessage(content="Goodbye! Have a great day!")
        elif "how are you" in user_content_lower:
            return AIMessage(content="I'm doing well, thank you! How can I assist you?")
        elif "joke" in user_content_lower:
            return AIMessage(content="Why don't scientists trust atoms? Because they make up everything! 😄")
        elif "weather" in user_content_lower:
            return AIMessage(content="I'm sorry, I don't have access to current weather information.")
        else:
            return AIMessage(content=f"I understand you said: '{user_content}'. How can I help you with that?")


# 全局LLM管理器实例
llm_manager = LLMManager()


# 便捷函数
def get_llm():
    """获取LLM实例的便捷函数"""
    return llm_manager.get_llm()


def get_llm_info():
    """获取LLM信息"""
    return {
        "type": llm_manager.get_llm_type(),
        "is_mock": llm_manager.is_mock(),
        "azure_deployment": Config.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
        "azure_endpoint": Config.AZURE_OPENAI_ENDPOINT,
        "api_version": Config.AZURE_OPENAI_API_VERSION,
        "temperature": Config.LLM_TEMPERATURE,
        "max_tokens": Config.LLM_MAX_TOKENS
    }


# 配置函数
def configure_llm(azure_deployment: Optional[str] = None,
                  temperature: Optional[float] = None,
                  max_tokens: Optional[int] = None,
                  azure_endpoint: Optional[str] = None,
                  api_version: Optional[str] = None):
    """动态配置Azure OpenAI LLM参数"""
    if azure_deployment:
        os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = azure_deployment
        Config.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = azure_deployment
    if temperature is not None:
        os.environ["LLM_TEMPERATURE"] = str(temperature)
        Config.LLM_TEMPERATURE = temperature
    if max_tokens is not None:
        os.environ["LLM_MAX_TOKENS"] = str(max_tokens)
        Config.LLM_MAX_TOKENS = max_tokens
    if azure_endpoint is not None:
        os.environ["AZURE_OPENAI_ENDPOINT"] = azure_endpoint
        Config.AZURE_OPENAI_ENDPOINT = azure_endpoint
    if api_version is not None:
        os.environ["AZURE_OPENAI_API_VERSION"] = api_version
        Config.AZURE_OPENAI_API_VERSION = api_version

    # 重新初始化LLM
    llm_manager._llm = None
    llm_manager._initialize_llm()

    return llm_manager.get_llm()
