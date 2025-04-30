import pandas as pd
from collections import Counter

# Load the full augmented dataset
df = pd.read_csv("augmented_perfume_dataset_with_names.tsv", sep="\t")

# Only keep real winning perfumes
real_winning = df[df['Label'] == 'Winning'].copy()

# Function to calculate proportion of notes in a specific column
def calc_note_proportion(df_subset, column):
    all_notes = [note for row in df_subset[column].dropna() for note in row.split(',')]
    counter = Counter(all_notes)
    total = sum(counter.values())
    return sorted([(note, count / total) for note, count in counter.items()], key=lambda x: x[1], reverse=True)

# Calculate proportions
top_props = calc_note_proportion(real_winning, 'Top')
heart_props = calc_note_proportion(real_winning, 'Heart')
base_props = calc_note_proportion(real_winning, 'Base')

# Show top 10 most frequent notes in each category
print("\nTop Notes in Real Winning Perfumes:")
for note, prop in top_props[:10]:
    print(f"{note}: {prop:.2%}")

print("\nHeart Notes in Real Winning Perfumes:")
for note, prop in heart_props[:10]:
    print(f"{note}: {prop:.2%}")

print("\nBase Notes in Real Winning Perfumes:")
for note, prop in base_props[:10]:
    print(f"{note}: {prop:.2%}")


# Save proportions to a tab-delimited file
with open("winning_note_proportions.tsv", "w") as f:
    f.write("Note_Type\tNote\tProportion\n")

    for note, prop in top_props:
        f.write(f"Top\t{note}\t{prop:.6f}\n")

    for note, prop in heart_props:
        f.write(f"Heart\t{note}\t{prop:.6f}\n")

    for note, prop in base_props:
        f.write(f"Base\t{note}\t{prop:.6f}\n")
