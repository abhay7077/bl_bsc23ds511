import hashlib
import json
from time import time
import streamlit as st

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.create_block(previous_hash='1', proof=100)  # Genesis block

    def create_block(self, proof, previous_hash):
        block = Block(len(self.chain) + 1, time(), self.current_data, previous_hash)
        self.current_data = []  # Reset current data
        self.chain.append(block)
        return block

    def add_parcel_tracking(self, parcel_id, status, location):
        self.current_data.append({
            'parcel_id': parcel_id,
            'status': status,
            'location': location,
            'timestamp': time()
        })
        return self.last_block.index + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def to_dict(self):
        return [block.__dict__ for block in self.chain]

# Initialize the blockchain
blockchain = Blockchain()

# Streamlit UI
st.title("Parcel Delivery Tracking Blockchain")

# Input form for adding parcel tracking information
with st.form(key='parcel_form'):
    parcel_id = st.text_input("Parcel ID")
    status = st.text_input("Status")
    location = st.text_input("Location")
    submit_button = st.form_submit_button(label='Add Parcel Tracking')

    if submit_button:
        block_index = blockchain.add_parcel_tracking(parcel_id, status, location)
        st.success(f'Parcel tracking information added to Block {block_index}.')

# Display the blockchain
if st.button('View Blockchain'):
    chain_data = blockchain.to_dict()
    st.write("Current Blockchain:")
    for block in chain_data:
        st.write(f"Block {block['index']}:")
        st.write(f"Timestamp: {block['timestamp']}")
        st.write(f"Data: {block['data']}")
        st.write(f"Hash: {block['hash']}")
        st.write(f"Previous Hash: {block['previous_hash']}")
        st.write("---")
