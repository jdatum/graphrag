# graphrag_vertex/vertex_embed.py
import vertexai
from vertexai.language_models import TextEmbeddingModel
from graphrag.language_model.protocol.base import EmbeddingModel as EmbedProto
from graphrag.config.models.language_model_config import LanguageModelConfig

class VertexEmbedding(EmbedProto):
    def __init__(self, *, name: str, config: LanguageModelConfig, **kw):
        self.config = config
        # self.project_id = os.getenv("PROJECT_ID")
        # self.location = os.getenv("LOCATION")
        # vertexai.init(
        #     project=self.project_id,
        #     location=self.location,
        # )
        self._model = TextEmbeddingModel.from_pretrained(config.model)

    async def aembed_batch(self, text_list, **kw):
        res = await self._model.get_embeddings_async(text_list, **kw)
        return [v.values for v in res]

    def embed_batch(self, text_list, **kw):
        res = self._model.get_embeddings(text_list, **kw)
        return [v.values for v in res]

    async def aembed(self, text, **kw): return (await self.aembed_batch([text]))[0]
    def embed(self, text, **kw): return self.embed_batch([text])[0]
