import tkinter as tk
from tkinter import ttk
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import pickle

# Load the Keras model
model = load_model('perfume_cnn_model.keras')

# Load the tokenizer (assuming it's used for processing the input)
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Load note data from the TSV file
def load_note_data():
    note_data = {'Top': {}, 'Heart': {}, 'Base': {}}
    df = pd.read_csv('winning_note_proportions.tsv', sep='\t')
    
    for _, row in df.iterrows():
        note_type = row['Note_Type']
        note = row['Note']
        proportion = row['Proportion']
        
        if note_type in note_data:
            note_data[note_type][note] = proportion
    
    return note_data

note_data = load_note_data()

# Create the GUI window
window = tk.Tk()
window.title("Fragrance Combination Predictor")

# Function to get the proportions for selected notes
def get_proportions():
    top_note = top_combobox.get()
    heart_note = heart_combobox.get()
    base_note = base_combobox.get()

    top_proportion = note_data["Top"].get(top_note, 0)
    heart_proportion = note_data["Heart"].get(heart_note, 0)
    base_proportion = note_data["Base"].get(base_note, 0)

    # Process input for the model (you can use the tokenizer here if needed)
    input_data = np.array([[top_proportion, heart_proportion, base_proportion]])

    # Predict using the model (you can modify this depending on how your model works)
    prediction = model.predict(input_data)

    # Display the prediction result
    result_label.config(text=f"Winning Chance: {prediction[0][0]:.2f}%")

# Create dropdowns (comboboxes) for selecting notes
top_combobox = ttk.Combobox(window, values=list(note_data["Top"].keys()))
top_combobox.set("Bergamot")  # Default selection (can be changed dynamically)
top_combobox.grid(row=0, column=1)

heart_combobox = ttk.Combobox(window, values=list(note_data["Heart"].keys()))
heart_combobox.set("Jasmine")  # Default selection
heart_combobox.grid(row=1, column=1)

base_combobox = ttk.Combobox(window, values=list(note_data["Base"].keys()))
base_combobox.set("Musk")  # Default selection
base_combobox.grid(row=2, column=1)

# Create labels for each note type
tk.Label(window, text="Top Note:").grid(row=0, column=0)
tk.Label(window, text="Heart Note:").grid(row=1, column=0)
tk.Label(window, text="Base Note:").grid(row=2, column=0)

# Button to trigger the prediction
predict_button = tk.Button(window, text="Predict Winning Chance", command=get_proportions)
predict_button.grid(row=3, column=1)

# Label to display the result
result_label = tk.Label(window, text="Winning Chance: N/A")
result_label.grid(row=4, column=1)

# Start the GUI loop
window.mainloop()

