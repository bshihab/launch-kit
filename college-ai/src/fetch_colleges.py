from flask import Request
from datetime import datetime
import os
import requests
from google.cloud import firestore

# Fetch colleges for a single state
def fetch_colleges_by_state(state, page=0, per_page=100):
    # Your existing fetch_colleges_by_state function code here
    ...

# Upload colleges to Firestore
def upload_to_firestore(colleges):
    # Your existing upload_to_firestore function code here
    ...

# Entry-point function
def update_colleges(request: Request):
    """
    HTTP-triggered Cloud Function to update college data.
    """
    STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
              "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND",
              "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    all_colleges = []

    for state in STATES:
        page = 0
        while True:
            colleges = fetch_colleges_by_state(state, page=page, per_page=100)
            if not colleges:
                break
            all_colleges.extend(colleges)
            page += 1

    upload_to_firestore(all_colleges)
    return "Colleges updated successfully!", 200
