# graphrag_vertex/vertex_chat.py
import asyncio
import vertexai
from vertexai.language_models import ChatModel
from tenacity import retry, wait_exponential, stop_after_attempt
from graphrag.language_model.response.base import (
    BaseModelOutput, BaseModelResponse, ModelResponse
)
from graphrag.language_model.protocol.base import ChatModel as ChatProto
from graphrag.config.models.language_model_config import LanguageModelConfig
from .vertex_auth import ApiKeyCreds

class VertexChat(ChatProto):
    def __init__(self, *, name: str, config: LanguageModelConfig, **kw):
        if config.api_key is None:
            raise ValueError("vertex ai api key not set.")
        creds = ApiKeyCreds(config.api_key)
        vertexai.init(
            project=creds.project_id,
            location=creds.location,
            credentials=creds,
        )
        self._chat_model = ChatModel.from_pretrained(config.model)
        self.config = config

    @retry(wait=wait_exponential(multiplier=1.5), stop=stop_after_attempt(5))
    async def achat(self, prompt: str, history=None, **kw) -> ModelResponse:
        sess = self._chat_model.start_chat()
        resp = await sess.send_message_async(prompt, **kw)
        return BaseModelResponse(
            output=BaseModelOutput(
                content=resp.text,
                full_response=resp.__dict__
            ),
            parsed_response=None
        )

    def chat(self, prompt: str, history=None, **kw) -> ModelResponse:
        loop = asyncio.get_event_loop() \
            if asyncio.get_event_loop().is_running() else asyncio.new_event_loop()
        return loop.run_until_complete(self.achat(prompt, history, **kw))