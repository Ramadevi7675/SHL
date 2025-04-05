# app.py

import streamlit as st
import pandas as pd
from matching_engine import recommend_assessments

# Load your SHL catalog CSV
df = pd.read_csv("shl_sample_assessments.csv")

# Streamlit App UI
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title(" SHL Assessment Recommender")

# Text input from user
query = st.text_area("Enter a Job Description or Role Title")

if st.button("Recommend Assessments"):
    if query.strip() != "":
        results = recommend_assessments(query, csv_path="shl_sample_assessments.csv")
        
        if not results.empty:
            st.success("Recommended Assessments:")
            st.dataframe(results)
        else:
            st.warning("No matching assessments found. Try a different input.")
    else:
        st.error(" Please enter some text.")
