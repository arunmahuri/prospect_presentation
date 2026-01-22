from chromadb import PersistentClient
from src.utils.config import ChromaConfig, IntentHQConfig

cfg = ChromaConfig()
intenthq_cfg = IntentHQConfig()
do_force_index = intenthq_cfg.do_force_index

def intenthq_index_exists() -> bool:
    if do_force_index:
        return False
    client = PersistentClient(path=cfg.persist_dir)
    try:
        collection = client.get_collection(cfg.intenthq_collection)
        count = collection.count()
        return count > 0
    except Exception:
        return False