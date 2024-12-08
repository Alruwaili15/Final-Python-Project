import pandas as pd

# Path to the Excel file with detections
results_excel_path = "C://Users//ength//Desktop//29th Projects//ASU Manufacturing Program//MFG598 Python//Projecct Work//FinalPokerCardsDetection4Video//PokerCardDataset//PokerCardCalculator//Results.xlsx"

# Scoring Rules for Sun, Huk, and Mash
sun_card_scores = {
    "2": 0, "3": 0, "4": 0, "5": 0, "6": 0,
    "7": 1, "8": 1, "9": 1,
    "J": 2, "Q": 3, "K": 4, "10": 10, "A": 11
}

huk_card_scores = {
    "2": 1, "3": 1, "4": 1, "5": 1, "6": 1,
    "7": 5, "8": 5, "9": 19,
    "J": 10, "Q": 10, "K": 10, "10": 10, "A": 15
}

mash_card_scores = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9,
    "J": 15, "Q": 15, "K": 15, "10": 10, "A": 20
}

def calculate_card_points(excel_path):
    # Ask for the game type
    game_type = input("Enter the game type (Sun, Huk, or Mash): ").strip().lower()
    if game_type == "sun":
        card_scores = sun_card_scores
        print("Using Sun scoring rules.")
    elif game_type == "huk":
        card_scores = huk_card_scores
        print("Using Huk scoring rules.")
    elif game_type == "mash":
        card_scores = mash_card_scores
        print("Using Mash scoring rules.")
    else:
        print("Invalid game type. Please enter 'Sun', 'Huk', or 'Mash'.")
        return

    # Load the Excel file
    try:
        df = pd.read_excel(excel_path)
        print("Excel file loaded successfully.")
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Extract labels and remove duplicates
    unique_labels = df['label'].unique()
    print(f"Unique labels detected: {unique_labels}")

    # Calculate points
    total_points = 0
    card_details = []
    for label in unique_labels:
        # Extract the card value (first characters before the suit)
        card_value = ''.join(filter(str.isalnum, label)).strip().upper()
        # Use the first numeric or character sequence before the suit
        card_value = card_value[:-1] if card_value[-1].isalpha() else card_value
        card_score = card_scores.get(card_value, 0)  # Default to 0 if not found
        total_points += card_score
        card_details.append({"label": label, "points": card_score})

    # Display detailed card scores
    print("\nCard Scores:")
    for card in card_details:
        print(f"Card: {card['label']} -> Points: {card['points']}")

    print(f"\nTotal Points: {total_points}")

    # Save results to a new Excel file
    output_path = "C://Users//ength//Desktop//29th Projects//ASU Manufacturing Program//MFG598 Python//Projecct Work//FinalPokerCardsDetection4Video//PokerCardDataset//PokerCardCalculator//CardScores.xlsx"
    try:
        result_df = pd.DataFrame(card_details)
        result_df.to_excel(output_path, index=False)
        print(f"Card scores saved to: {output_path}")
    except Exception as e:
        print(f"Error saving card scores to Excel: {e}")

if __name__ == "__main__":
    calculate_card_points(results_excel_path)
