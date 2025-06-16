# Automated_Book_System
This project implements an automated workflow for book publication, enabling content versioning, AI-assisted review, human editing, and semantic search. The application uses a Streamlit frontend for user interaction, ChromaDB for persistent document storage, and SentenceTransformers for generating embeddings to support semantic search.

Demo Link : https://drive.google.com/file/d/10XAlsHR6KCWsWkmTCe_7b53pqcoU2hY-/view?usp=drive_link

## Features
1. Version Management: Store and retrieve multiple versions of book content (original, ai_spun, ai_reviewed, human_edited) in ChromaDB.
2. AI-Reviewed Content Display: View the latest AI-reviewed version of a manuscript.
3. Human Editing: Edit AI-reviewed content and save as a human_edited version, with prepopulation to ensure relevance.
4. Version History: Browse all stored versions with timestamps and document IDs.
5. Semantic Search: Search across versions using natural language queries, powered by SentenceTransformer embeddings.
6. Persistent Storage: Use ChromaDB to store documents and embeddings locally.

## Usage
### View AI-Reviewed Content:
1. The "AI-Reviewed Content" section displays the latest ai_reviewed version of the manuscript.
2. If no content appears, ensure the AI workflow (e.g., main.py) has processed the manuscript.
### Edit Content:
1. The "Edit Content" section prepopulates with the ai_reviewed text.
2. Make changes and click "Save Edited Version" to store as human_edited in ChromaDB.
3. A success message confirms the save.
### View Version History:
1. Click "Show All Versions" to see all stored versions (original, ai_spun, ai_reviewed, human_edited).
2. Each version is displayed with its document ID and save timestamp, sorted newest to oldest.
### Search Versions:
1. Enter a query (e.g., "latest chapter version") in the "Search Versions" section.
2. Results show matching versions with timestamps, based on semantic similarity.
   
## Technical Details
*Frontend:* 
Streamlit provides an interactive web interface for human review and editing. 
*Backend:*
1. ChromaDB: Persistent vector database for storing documents and embeddings, with upsert to overwrite versions (e.g., human_edited).
2. SentenceTransformers: Uses the all-MiniLM-L6-v2 model to generate embeddings for semantic search and version storage.
3. Storage: Documents are stored in data/chromadb with metadata (version type, timestamp) and embeddings.
4. Logging: Comprehensive logging for debugging save/retrieve operations.
