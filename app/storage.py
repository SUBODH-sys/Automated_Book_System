import chromadb
from sentence_transformers import SentenceTransformer
import logging
from datetime import datetime  # Added for timestamps

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize ChromaDB with persistent storage
client = chromadb.PersistentClient(path="data/chromadb")  # Store database in data/chromadb
try:
    collection = client.get_or_create_collection("book_versions")
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB collection: {str(e)}")
    raise

try:
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer: {str(e)}")
    raise Exception("SentenceTransformer initialization failed. Check PyTorch and dependency versions.")

def save_version(doc_id, content, version_name):
    """
    Save content to ChromaDB with embeddings and metadata, overwriting existing document if present.
    """
    try:
        embedding = embedder.encode(content).tolist()
        metadata = {"version": version_name, "timestamp": datetime.utcnow().isoformat()}
        collection.upsert(  # Changed from add to upsert
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id]
        )
        logger.info(f"Saved document {doc_id} with version {version_name} at {metadata['timestamp']}")
        logger.info(f"Current collection contents: {collection.get(include=['documents', 'metadatas'])}")
    except Exception as e:
        logger.error(f"Failed to save to ChromaDB: {str(e)}")
        raise Exception(f"Failed to save to ChromaDB: {str(e)}")

def retrieve_version(version_id=None, all_versions=False):
    """
    Retrieve specific or all versions from ChromaDB.
    """
    try:
        if all_versions:
            result = collection.get(include=["documents", "metadatas"])
        else:
            result = collection.get(ids=[version_id], include=["documents", "metadatas"])
        logger.info(f"Retrieved version {version_id or 'all'}: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to retrieve from ChromaDB: {str(e)}")
        return {"documents": [], "metadatas": []}