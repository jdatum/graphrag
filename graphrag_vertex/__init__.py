# __init__.py (graphrag_vertex)
from graphrag.language_model.factory import ModelFactory
from .vertex_chat import VertexChat
from .vertex_embed import VertexEmbedding

ModelFactory.register_chat("vertex_chat", lambda **kw: VertexChat(**kw))
ModelFactory.register_embedding("vertex_embed", lambda **kw: VertexEmbedding(**kw))
