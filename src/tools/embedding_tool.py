from typing import List
from src.utils.chroma_setup import VectorStore, Document
from src.utils.llm_setup import embeddings_model
from loguru import logger

vector_store = VectorStore()

def add_documents(documents, metadatas, collection_name):
    """Add documents to the correct backend."""
    logger.info(f"Adding documents to collection '{collection_name}'")
    collection = vector_store.get_or_create_collection(collection_name)

    logger.debug(f"Using collection: {collection_name}")

    ids = [f"{collection_name}_{i}" for i in range(len(documents))]
    embeddings = embeddings_model.embed_documents(documents)

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    logger.info(f"Added {len(documents)} documents to collection '{collection_name}'")

def search(collection_name, query, k=5):
    """Semantic search in the correct backend."""
    logger.info(f"Searching in collection '{collection_name}' for query: {query}")
    try:
        collection = vector_store.get_or_create_collection(collection_name)
        query_embedding = embeddings_model.embed_query(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        logger.info(f"Search returned {len(results['documents'][0])} results")

        docs = []
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            docs.append(Document(page_content=doc, metadata=metadata))

        logger.debug(f"Search results: {docs}")
        return docs

    except Exception as e:
        print(f"Search error: {e}")
        return []

# db = get_chroma(collection_name)
# ids = [f"{collection_name}_{i}" for i in range(len(texts))]
# db.add_texts(texts=texts, metadatas=metadatas, ids=ids)
# return ids