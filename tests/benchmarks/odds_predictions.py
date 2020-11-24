import pandas as pd

# ----------------------------------------------------------------------------
# This file is for calculating accuracy in odds-predictions made by bookmakers
# ----------------------------------------------------------------------------

if __name__ == '__main__':
    # Import raw dataset as dataframe
    data = pd.read_csv("../../data/datasets/raw/epl2020.csv")
    df = pd.DataFrame(data)

    correct_pred = 0

    # Iterate trough dataset calculating bookmaker accuracy
    for i, row in df.iterrows():
        home_team = row["h_a"] == "h"
        result = row["result"]  # actual result
        odds_pred = row[["B365H.x", "B365D.x", "B365A.x"]].astype(float).argmin()  # lowest odds is predicted winner

        # if predicted winner is home team
        if odds_pred == 0:

            if home_team & (result == "w"):
                correct_pred += 1
            elif (not home_team) & (result == "l"):
                correct_pred += 1

        # if predicted draw
        elif odds_pred == 1:

            if result == "d":
                correct_pred += 1

        # if predicted winner is away team
        elif odds_pred == 2:

            if home_team & (result == "l"):
                correct_pred += 1
            elif (not home_team) & (result == "w"):
                correct_pred += 1

    print("Accuracy: ", round(correct_pred / len(df), 2) * 100, "%")
