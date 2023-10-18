from .db import db

collection = db.collection('raw_data')

# get all raw data
def get_all_raw_data():
    res = collection.get()
    data = []
    for entry in res:
        data.append(entry.to_dict())
    return data

# Insert a single data entry into firestore
def insert_raw_data(data):
    batch = db.batch()

    # Batch all data entries 
    for entry in data:
        batch.set(collection.document(), entry)
    
    res = batch.commit()
    return res

