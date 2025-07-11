import graphrag_vertex
from pathlib import Path
import asyncio
import graphrag.api as api
from graphrag.config.load_config import load_config

cfg = load_config(Path("voc_test"))

async def main():
    await api.build_index(config=cfg)

asyncio.run(main())
