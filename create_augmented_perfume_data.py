import pandas as pd
import random
from faker import Faker

# Initialize Faker for generating fake names
fake = Faker()

# File path
file_path = "perfume_data.csv"

# Step 1: Read the file using tab delimiter
df = pd.read_csv(file_path, delimiter='\t', engine='python')

# Step 2: Handle missing 'Gender' values
df['Gender'].fillna('Unknown', inplace=True)

# Step 3: Capitalize first letter of each part of notes (including after underscores)
def capitalize_note(note_str):
    try:
        return ','.join([
            '_'.join([word.capitalize() for word in note.split('_')])
            for note in note_str.split(',')
        ])
    except:
        return note_str  # In case of non-string values (e.g., NaN)

df['Top'] = df['Top'].apply(capitalize_note)
df['Heart'] = df['Heart'].apply(capitalize_note)
df['Base'] = df['Base'].apply(capitalize_note)

# Step 4: Print to verify
print("First few rows after proper capitalization:")
print(df[['Top', 'Heart', 'Base']].head())

# Fill missing values in Top, Heart, and Base columns
df['Top'] = df['Top'].fillna('')
df['Heart'] = df['Heart'].fillna('')
df['Base'] = df['Base'].fillna('')

# Extract all unique notes from the dataset
def extract_unique_notes(column):
    notes = set()
    for row in df[column]:
        notes.update([note.strip().lower() for note in row.split(',') if note.strip()])
    return notes

# Get unique notes for each category
top_notes = extract_unique_notes("Top")
heart_notes = extract_unique_notes("Heart")
base_notes = extract_unique_notes("Base")

# Combine all notes
all_notes = list(top_notes.union(heart_notes).union(base_notes))

# Function to generate fake perfume with random name
def generate_fake_perfume():
    top = ','.join(random.sample(all_notes, random.randint(1, 4)))  # Random number of notes
    heart = ','.join(random.sample(all_notes, random.randint(1, 4)))
    base = ','.join(random.sample(all_notes, random.randint(1, 4)))
    name = fake.first_name() + " " + random.choice(["Mist", "Flame", "Essence", "Aura", "Whisper"])
    return {"Name": name, "Top": top, "Heart": heart, "Base": base, "Label": "Losing"}


# Generate fake perfumes (same count as real perfumes)

fake_perfumes = pd.DataFrame([generate_fake_perfume() for _ in range(len(df))])

fake_perfumes['Top'] = fake_perfumes['Top'].apply(capitalize_note)
fake_perfumes['Heart'] = fake_perfumes['Heart'].apply(capitalize_note)
fake_perfumes['Base'] = fake_perfumes['Base'].apply(capitalize_note)

df['Label'] = 'Winning'  # Label real perfumes as "Winning"
# Combine real and fake perfumes (keeping the same structure, including original names for real perfumes)
augmented_df = pd.concat([df[['Name', 'Top', 'Heart', 'Base', 'Label']], fake_perfumes[['Name', 'Top', 'Heart', 'Base', 'Label']]], ignore_index=True)

# Shuffle the data to mix real and fake perfumes
augmented_df = augmented_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the augmented dataset as tab-delimited
augmented_df.to_csv("augmented_perfume_dataset_with_names.tsv", sep='\t', index=False)

print("Augmented dataset saved as 'augmented_perfume_dataset_with_names.tsv'.")

