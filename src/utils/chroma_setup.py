
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb import chromadb
from src.utils.config import ChromaConfig

chroma_cfg = ChromaConfig()


class VectorStore:
    def __init__(self):
        # Persistent DB for IntentHQ
        self.persistent_client = chromadb.PersistentClient(path=chroma_cfg.persist_dir)

        # In-memory DB for prospect data
        self.memory_client = chromadb.Client()   # <-- no path = in-memory

        # Cache of loaded collections
        self.collections = {}

    def get_or_create_collection(self, collection_name):
        """
        Route collections:
        - intenthq_* → persistent Chroma
        - prospect_* → in-memory Chroma
        """
        if collection_name in self.collections:
            return self.collections[collection_name]

        # Decide backend based on collection name
        if collection_name.startswith("intenthq"):
            client = self.persistent_client
        else:
            client = self.memory_client

        # Try to load existing collection
        try:
            collection = client.get_collection(name=collection_name)
        except:
            collection = client.create_collection(name=collection_name)

        self.collections[collection_name] = collection
        return collection


class Document:
    """Simple document class to match LangChain format."""
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}