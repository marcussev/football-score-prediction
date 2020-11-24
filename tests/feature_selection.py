from sklearn.neural_network import MLPClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
import visualizer


# ---------------------------------------------------------------------
# This file contains methods for analyzing feature importance in models
# ---------------------------------------------------------------------

# Estimates feature importance in MLP-models
def get_mlp_importance(dataset):
    data = dataset.drop(["teamA", "teamB"], axis=1)
    columns = data.iloc[:, 2:].columns  # Container for column names

    # Split into input and output
    X = data.iloc[:, 2:].values
    y = []
    for i in range(len(X)):
        score = data.iloc[i, 0:2].values
        # team A win
        if int(score[0]) > int(score[1]):
            y.append([1, 0, 0])

        # team B win
        elif int(score[0]) < int(score[1]):
            y.append([0, 0, 1])

        # draw
        else:
            y.append([0, 1, 0])

    # Model
    model = MLPClassifier(max_iter=500)
    model.fit(X, y)
    print(model.score(X, y))

    # perform permutation importance
    results = permutation_importance(model, X, y, scoring='accuracy')

    # get importance
    importance = results.importances_mean

    # summarize feature importance
    for i, v in enumerate(importance):
        print("%s, Score(goals teamA): %.5f" % (columns[i], v))

    # plot feature importance
    visualizer.plot_feature_importance(importance, columns,
                                       "Classification", "./results/graphs/feature_importance_mlp.png")


# Estimates feature importance in linear regression models
def get_regression_importance(dataset):
    # Import full dataset
    data = dataset.drop(["teamA", "teamB"], axis=1)
    columns = data.iloc[:, 2:].columns

    # Split into input and output
    X, y = data.iloc[:, 2:].values, data.iloc[:, 0:2].values

    # Model
    model = LinearRegression()
    model.fit(X, y)

    # Estimate feature importance
    importance = model.coef_
    print("Feature importance for goals scored by teamA:\n")
    for i, v in enumerate(importance[0]):
        print("%s, Score(goals teamA): %.5f" % (columns[i], v))

    print("\nFeature importance for goals scored by teamB:\n")
    for i, v in enumerate(importance[1]):
        print("%s, Score(goals teamB): %.5f" % (columns[i], v))

    # Plot feature importance for each score (goals team A and goals team B)
    visualizer.plot_feature_importance(importance[0], columns, "Goals teamA",
                                       "./results/graphs/feature_importance_reg_a.png")
    visualizer.plot_feature_importance(importance[1], columns, "Goals teamB",
                                       "./results/graphs/feature_importance_reg_b.png")
