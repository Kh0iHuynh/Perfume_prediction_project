import sys
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

def load_tokenizer(path='tokenizer.pkl'):
    with open(path, 'rb') as f:
        return pickle.load(f)

def prepare_input(full_text, tokenizer, max_len):
    sequence = tokenizer.texts_to_sequences([full_text])
    padded = pad_sequences(sequence, maxlen=max_len, padding='post')
    return padded

def main():
    if len(sys.argv) != 4:
        print("Usage: python load_and_predict.py \"TopNotes\" \"HeartNotes\" \"BaseNotes\"")
        print("Each argument should be a comma-separated list of notes for that layer.")
        sys.exit(1)

    top = sys.argv[1]
    heart = sys.argv[2]
    base = sys.argv[3]

    # Combine into one input string
    full_input = f"{top},{heart},{base}"

    # Load tokenizer and model
    tokenizer = load_tokenizer("tokenizer.pkl")
    model = load_model("perfume_cnn_model.keras")

    # Use the same max_len as in training
    max_len = 50  # Adjust if your training used a different value

    # Prepare input
    X_input = prepare_input(full_input, tokenizer, max_len)

    # Predict
    prediction = model.predict(X_input)[0][0]

    # Print result
    print(f"\nNotes Combination: '{full_input}'")
    print(f"Winning Chance: {prediction:.4f}")

if __name__ == "__main__":
    main()

