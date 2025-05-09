import streamlit as st
from pymongo import MongoClient
import json
from bson import json_util

MONGO_URI = "mongodb://localhost:27021"
DB_NAME = "twitter"
COLLECTION_NAME = "tweets"

client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

st.title("View MongoDB Documents")

if st.button("Load Documents"):
    documents = list(collection.find().limit(10))
    if documents:
        st.subheader("First 10 Documents:")
        st.json(json.loads(json_util.dumps(documents)))
    else:
        st.info("No documents found.")
