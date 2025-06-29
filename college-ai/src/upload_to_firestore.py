import json
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()

# Load college data from JSON file
with open('colleges.json', 'r') as file:
    colleges = json.load(file)

# Upload or update data in Firestore
for college in colleges:
    if "id" not in college:
        print(f"Skipping college due to missing ID: {college}")
        continue
    # Convert the ID to a string
    doc_ref = db.collection('colleges').document(str(college['id']))

    # Check if the document already exists
    existing_doc = doc_ref.get()
    if existing_doc.exists and existing_doc.to_dict() == college:
        print(f"No changes for college {college['school.name']} (ID: {college['id']})")
        continue

    # Add or update the document
    doc_ref.set(college)
    print(f"Uploaded/Updated: {college['school.name']} (ID: {college['id']})")

print("Data upload/update completed successfully!")
