import matplotlib.pyplot as plt
import numpy as np


# ------------------------------------------
# This file contains methods for visualizing with matplotlib

# Uncomment plt.savefig() to save your visualisations
# ------------------------------------------

# Visualize loss throughout training and testing
def plot_loss(epochs, loss, save_path):
    plt.plot(np.linspace(1, epochs, epochs), loss)
    plt.xlabel("epochs")
    plt.ylabel("loss")
    plt.suptitle("Average loss per epoch")
    # plt.savefig(save_path)
    plt.show()


# Visualize accuracy throughout training and testing
def plot_accuracy(epochs, accuracy, save_path):
    plt.plot(np.linspace(1, epochs, epochs), accuracy)
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.suptitle("Accuracy per epoch")
    # plt.savefig(save_path)
    plt.show()


# Visualize importance of each feature
def plot_feature_importance(importance, feature_names, title, save_path):
    plt.bar([x for x in feature_names], importance)
    plt.xlabel("Feature")
    plt.xticks(rotation=90)
    plt.ylabel("Score")
    plt.suptitle(title)
    plt.savefig(save_path)
    plt.show()


# Visualize comparison of accuracy between models
def plot_comparison(accuracies, models, save_path):
    plt.barh([x for x in models], accuracies)
    plt.xlabel("Model")
    plt.xticks(rotation=90)
    plt.ylabel("Accuracy")
    plt.suptitle("Model comparison with benchmarks")
    for i, v in enumerate(accuracies):
        plt.text(v, i, str(v) + "%")
    plt.tight_layout()
    # plt.savefig(save_path)
    plt.show()
