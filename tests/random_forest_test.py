from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import pandas as pd
import numpy as np

# Read data from data from csv
data = pd.read_csv("../data/datasets/processed/games_full_data.csv")
data = data.drop(["teamA", "teamB"], axis=1)
x_data = data.iloc[:, 3:].values
y_data = data.iloc[:, 1:3].values

# Split into random training and testing subsets
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.25, random_state=0)

# Feature scaling
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Create a random regressor
regressor = RandomForestRegressor(n_estimators=20, random_state=0)

# Train the model using the training sets y_pred=clf.predict(X_test)
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)

# Convert regressor predictions in to regular football scores and check accuracy
correct_pred = 0
scores = []
for i in range(len(y_pred)):
    res_pred = [int(y_pred[i, 0]), int(y_pred[i, 1])]
    res_true = [y_test[i, 0], y_test[i, 1]]

    if (res_pred[0] > res_pred[1]) & (res_true[0] > res_true[1]):
        correct_pred += 1
    elif (res_pred[0] < res_pred[1]) & (res_true[0] < res_true[1]):
        correct_pred += 1
    elif (res_pred[0] == res_pred[1]) & (res_true[0] == res_true[1]):
        correct_pred += 1

    scores.append(res_pred)

# Accuracy
print('Accuracy:', round((correct_pred/len(y_pred)), 2))
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
