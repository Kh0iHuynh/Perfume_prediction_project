import argparse
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

def validate_notes(notes_str, label):
    if not notes_str or not any(note.strip() for note in notes_str.split(',')):
        print(f"Error: '{label}' notes cannot be empty. Provide a comma-separated string of scent names.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Predict the winning chance of a perfume based on its scent composition.\n\n"
            "Each argument must be a **single combination** of notes, formatted as a comma-separated list.\n"
            "Example:\n"
            "  Top:   'Rose,Lemon'\n"
            "  Heart: 'Jasmine'\n"
            "  Base:  'Musk,Amber'\n\n"
            "This will predict for the combination: 'Rose,Lemon,Jasmine,Musk,Amber'"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("Top", type=str, help="Comma-separated string of top notes (e.g. 'Rose,Lemon')")
    parser.add_argument("Heart", type=str, help="Comma-separated string of heart notes (e.g. 'Jasmine,Lavender')")
    parser.add_argument("Base", type=str, help="Comma-separated string of base notes (e.g. 'Musk,Amber')")

    args = parser.parse_args()

    # Validate input early
    validate_notes(args.Top, "Top")
    validate_notes(args.Heart, "Heart")
    validate_notes(args.Base, "Base")

    # Combine all notes into one string
    full_input = f"{args.Top},{args.Heart},{args.Base}"

    # Load model & tokenizer after validation
    tokenizer = load_tokenizer("tokenizer.pkl")
    model = load_model("perfume_cnn_model.keras")

    # Use the same max_len as in training
    max_len = 50

    # Prepare input and predict
    X_input = prepare_input(full_input, tokenizer, max_len)
    prediction = model.predict(X_input)[0][0]

    # Output result
    print(f"\nNotes Combination: '{full_input}'")
    print(f"Winning Chance: {prediction:.4f}")

if __name__ == "__main__":
    main()

