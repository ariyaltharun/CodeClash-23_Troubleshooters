import streamlit as st
from ReviewAnalysis import sentiment_score
from RealTimeFaceDetection import start_capture


# Title
st.title("Click capture to mark your attendence")


# Capture button
capture = st.button("Capture")
if capture:
    start_capture()


# -------------------------- Dont touch ------------------------- #
# Suggection Box Form
with st.form("form"):
    st.write("Suggestion Box")
    test_area = st.text_area("Your Suggestion")
    
    # Submit button
    if st.form_submit_button("Submit"):
        st.write("Form submitted")

# Stores reviews in Review folder
sentiment_score(test_area)
# ---------------------------- Dont touch ends ----------------- #
