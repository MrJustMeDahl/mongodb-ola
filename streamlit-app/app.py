import streamlit as st
from pymongo import MongoClient
import json
from bson import json_util
from bson.code import Code

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

st.subheader("Insert New Tweet")
tweet_text = st.text_input("Enter tweet text")

if st.button("Submit Tweet"):
    if tweet_text.strip():
        result = collection.insert_one({"text": tweet_text})
        st.success(f"Tweet inserted with ID: {result.inserted_id}")
    else:
        st.warning("Tweet text cannot be empty.")


# map and reduce solution

if st.button("Top 10 Hashtags (MapReduce)"):

    map_fn = Code("""
    function () {
      if (this.entities && this.entities.hashtags) {
        this.entities.hashtags.forEach(function (hashtag) {
          emit(hashtag.text.toLowerCase(), 1);
        });
      }
    }
    """)

    reduce_fn = Code("""
    function (key, values) {
      return Array.sum(values);
    }
    """)

    result = collection.map_reduce(map_fn, reduce_fn, "hashtags_count")
    top_10 = result.find().sort("value", -1).limit(10)
    
    if top_10:
        st.subheader("Top 10 Hashtags (MapReduce):")
        st.json(json.loads(json_util.dumps(top_10)))
    else:
        st.info("No hashtags found.")

# aggregation solution

if st.button("Top 10 Hashtags"):
    pipeline = [
        # Filter out documents without hashtags
        { "$match": { "entities.hashtags": { "$exists": True, "$ne": [] } } },
        # Unwind takes each element of the array and creates a new document for each
        { "$unwind": "$entities.hashtags" },
        # Group hashtags by their text and count.
        { "$group": {
            "_id": { "$toLower": "$entities.hashtags.text" },
            "count": { "$sum": 1 }
        }},
        # Sort the hashtags by count from highest to lowest
        { "$sort": { "count": -1 } },
        # Only give top 10 hashtags
        { "$limit": 10 }
    ]

    top_hashtags = list(collection.aggregate(pipeline))
    if top_hashtags:
        st.subheader("Top 10 Hashtags:")
        st.json(top_hashtags)
    else:
        st.info("No hashtags found.")