import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load augmented file
df = pd.read_csv("augmented_perfume_dataset_with_names.tsv", sep='\t')

# Combine Top, Heart, Base into a single input text
df['Combined'] = df['Top'] + ',' + df['Heart'] + ',' + df['Base']

# Encode labels: Winning → 1, Losing → 0
label_encoder = LabelEncoder()
df['Label'] = label_encoder.fit_transform(df['Label'])  # Winning=1, Losing=0

# Tokenize the notes
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['Combined'])
sequences = tokenizer.texts_to_sequences(df['Combined'])

# Pad sequences
max_len = max(len(seq) for seq in sequences)
X = pad_sequences(sequences, maxlen=max_len, padding='post')
y = df['Label'].values

# Save tokenizer for future predictions
import pickle
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense

# Model parameters
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 50

# Define CNN model
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    Conv1D(filters=128, kernel_size=5, activation='relu'),
    GlobalMaxPooling1D(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# Train model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), batch_size=8)

# Save model
model.save("perfume_cnn_model.keras")



