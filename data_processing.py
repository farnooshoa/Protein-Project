from Bio import SeqIO
import os
from flask import Flask, render_template, request
import requests  # Import the requests library for HTTP requests
# Your existing code for data processing and model training

# Create Flask app
app = Flask(__name__)

# Define paths to your data files
fasta_file_path = "data/hemoglobin.fasta"
uniprot_ids = ["P68871", "Q9YH37", "O00203"]  # Replace with your list of UniProt IDs


def load_protein_sequences(fasta_file):
    """
    Load protein sequences from a FASTA file.
    
    Args:
        fasta_file (str): Path to the FASTA file.
        
    Returns:
        list of Bio.SeqRecord.SeqRecord: List of SeqRecord objects containing protein sequences.
    """
    sequences = list(SeqIO.parse(fasta_file, "fasta"))
    return sequences
def download_uniprot_data(uniprot_ids):
    """
    Download protein sequences from UniProt.
    
    Args:
        uniprot_ids (list of str): List of UniProt IDs.
        
    Returns:
        list of Bio.SeqRecord.SeqRecord: List of SeqRecord objects containing protein sequences.
    """
    sequences = []
    for uniprot_id in uniprot_ids:
        url = f'https://www.uniprot.org/uniprot/{uniprot_id}.fasta'
        response = requests.get(url)
        if response.status_code == 200:
            sequence = SeqIO.read(io.StringIO(response.text), 'fasta')
            sequences.append(sequence)
        else:
            print(f"Failed to download data for UniProt ID {uniprot_id}. Status code: {response.status_code}")
    return sequences

def preprocess_sequences(sequences):
    """
    Preprocess protein sequences.
    
    Args:
        sequences (list of Bio.SeqRecord.SeqRecord): List of SeqRecord objects containing protein sequences.
        
    Returns:
        list of str: List of protein sequences as strings.
    """
    preprocessed_sequences = [str(record.seq) for record in sequences]
    return preprocessed_sequences
# Load protein sequences
protein_sequences = load_protein_sequences(fasta_file_path)

# Preprocess sequences
preprocessed_sequences = preprocess_sequences(protein_sequences)

# Example: Print the first preprocessed sequence
print(preprocessed_sequences[0])
# Download UniProt data
uniprot_sequences = download_uniprot_data(uniprot_ids)

# Load protein sequences from a FASTA file
fasta_sequences = load_protein_sequences(fasta_file_path)

# Combine UniProt and FASTA sequences
all_sequences = uniprot_sequences + fasta_sequences

# Preprocess sequences
preprocessed_sequences = preprocess_sequences(all_sequences)

import numpy as np

def extract_amino_acid_composition(sequence):
    """
    Extract the amino acid composition of a protein sequence.
    
    Args:
        sequence (str): Protein sequence.
        
    Returns:
        dict: Dictionary containing the count of each amino acid.
    """
    amino_acids = set(sequence)
    composition = {aa: sequence.count(aa) for aa in amino_acids}
    return composition

def extract_features_for_ml(sequences):
    """
    Extract features from protein sequences for machine learning.
    
    Args:
        sequences (list of str): List of protein sequences.
        
    Returns:
        numpy.ndarray: 2D array of features (amino acid composition).
    """
    features = []
    for sequence in sequences:
        composition = extract_amino_acid_composition(sequence)
        feature_vector = np.array(list(composition.values()))
        features.append(feature_vector)
    
    return np.array(features)

# Example: Extract features from preprocessed sequences
features = extract_features_for_ml(preprocessed_sequences)

# Example: Print the features of the first protein
print(features[0])

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def train_linear_regression_model(features, labels):
    """
    Train a linear regression model for protein structure prediction.
    
    Args:
        features (numpy.ndarray): 2D array of features.
        labels (numpy.ndarray): 1D array of target labels.
        
    Returns:
        sklearn.linear_model.LinearRegression: Trained linear regression model.
    """
    model = LinearRegression()
    model.fit(features, labels)
    return model

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
# Train the linear regression model
model = train_linear_regression_model(X_train, y_train)
# Predict the targets for the test set
y_pred = model.predict(X_test)

# Calculate Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
# Assuming you have a trained model and X_test, y_test from previous steps

# Predict the targets for the test set
y_pred = model.predict(X_test)

# Calculate Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
