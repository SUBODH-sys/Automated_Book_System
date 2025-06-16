import logging
from app.storage import collection, embedder

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_versions(query, top_k=3):
    """
    Search for versions using a simple RL-inspired heuristic (similarity + recency).
    """
    try:
        query_embedding = embedder.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]  # Explicitly include distances
        )
        
        # Log query results for debugging
        logger.info(f"Query results: {results}")
        
        # Check if results are valid
        if not results or not results["documents"] or not results["documents"][0]:
            logger.warning("No documents found in ChromaDB.")
            return []
        
        # Rank by similarity and recency (simulated RL reward)
        ranked_results = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            # Use distance if available, else default to 0
            score = 0
            if results["distances"] and results["distances"][0]:
                score = results["distances"][0][results["documents"][0].index(doc)]
            # Boost score for newer versions
            version_order = {"original": 1, "ai_spun": 2, "ai_reviewed": 3, "human_edited": 4}
            recency_score = version_order.get(meta["version"], 0) * 0.1
            final_score = (1 - score) + recency_score if score else recency_score
            ranked_results.append((doc, meta, final_score))
        
        # Sort by final score
        ranked_results.sort(key=lambda x: x[2], reverse=True)
        return [{"document": doc, "metadata": meta} for doc, meta, _ in ranked_results[:top_k]]
    
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        return []