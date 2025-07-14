import vertexai
from vertexai.language_models import TextEmbeddingModel
from graphrag.config.models.language_model_config import LanguageModelConfig


model = TextEmbeddingModel.from_pretrained("text-multilingual-embedding-002")
res = model.get_embeddings(["データセットは大きければ大きいほどよい"])
print(type(res))
print(type(res[0]))
print(len(res[0].values))
