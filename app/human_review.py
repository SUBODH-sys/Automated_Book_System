import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.storage import retrieve_version, save_version
from app.search import search_versions
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Book Publication Workflow", layout="wide")

st.title("Automated Book Publication Workflow - Human Review")

# Display latest AI-reviewed content
st.subheader("AI-Reviewed Content")
latest_version = retrieve_version("ai_reviewed")
logger.info(f"AI-reviewed content retrieved: {latest_version}")
if latest_version and latest_version["documents"]:
    st.text_area("AI-Reviewed Text", latest_version["documents"][0], height=300, key="ai_text")
else:
    st.warning("No AI-reviewed content available. Ensure the workflow (`main.py`) has been run successfully.")

# Human editing
st.subheader("Edit Content")
default_text = latest_version["documents"][0] if latest_version and latest_version["documents"] else ""
edited_text = st.text_area("Enter your edited version", value=default_text, height=300, key="edit_text")
if st.button("Save Edited Version"):
    if edited_text.strip():
        save_version("human_edited", edited_text, "human_edited")
        st.success("Human-edited version saved to ChromaDB!")
        time.sleep(5)
        st.rerun()  # Refresh UI to show updated version history
    else:
        st.error("Please enter valid text to save.")

# Version history
st.subheader("Version History")
if st.button("Show All Versions"):
    versions = retrieve_version(all_versions=True)
    logger.info(f"Retrieved versions: {versions}")
    if versions and versions["documents"]:
        # Sort by timestamp (newest first) if available
        version_list = list(zip(versions["documents"], versions["metadatas"], versions["ids"]))
        version_list.sort(key=lambda x: x[1].get("timestamp", ""), reverse=True)
        for doc, meta, doc_id in version_list:
            timestamp = meta.get("timestamp", "No timestamp")
            with st.expander(f"Version: {meta['version']}"):
                st.text_area("Content", doc, height=200, key=f"{meta['version']}")
    else:
        st.warning("No versions available in ChromaDB.")

# Search versions
st.subheader("Search Versions")
query = st.text_input("Enter search query", value="latest chapter version")
if st.button("Search"):
    results = search_versions(query)
    logger.info(f"Search results for query '{query}': {results}")
    if results:
        for result in results:
            timestamp = result["metadata"].get("timestamp", "No timestamp")
            with st.expander(f"Version: {result['metadata']['version']}"):
                st.text_area("Content", result["document"], height=200, key=f"{result['metadata']['version']}_{timestamp}_search")
    else:
        st.warning("No results found.")