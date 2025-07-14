# graphrag_vertex/vertex_chat.py
import asyncio
from vertexai.generative_models import GenerativeModel
from tenacity import retry, wait_exponential, stop_after_attempt
from graphrag.language_model.response.base import (
    BaseModelOutput, BaseModelResponse, ModelResponse
)
from graphrag.language_model.protocol.base import ChatModel as ChatProto
from graphrag.config.models.language_model_config import LanguageModelConfig


class VertexChat(ChatProto):
    def __init__(self, *, name: str, config: LanguageModelConfig, **kw):
        self.config = config
        # self.project_id = os.getenv("PROJECT_ID")
        # self.location = os.getenv("LOCATION")
        # vertexai.init(
        #     project=self.project_id,
        #     location=self.location,
        # )
        self._chat_model = GenerativeModel(config.model)
        self.allowed_kw = {
            'generation_config',
            'safety_settings',
            'tools',
            'labels',
            'stream', 
        }

    # @retry(wait=wait_exponential(multiplier=1.5), stop=stop_after_attempt(5))
    async def achat(self, prompt: str, history=None, **kw) -> ModelResponse:
        sess = self._chat_model.start_chat(history=history)
        filtered_kw = {k: v for k, v in kw.items() if k in self.allowed_kw}
        resp = await sess.send_message_async(prompt, **filtered_kw)
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