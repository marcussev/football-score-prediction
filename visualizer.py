import matplotlib.pyplot as plt
import numpy as np


def plot_loss(epochs, loss):
    plt.plot(np.linspace(1, epochs, epochs), loss)
    plt.xlabel("epochs")
    plt.ylabel("loss")
    plt.suptitle("Average loss per epoch")
    plt.show()


def plot_accuracy(epochs, accuracy):
    plt.plot(np.linspace(1, epochs, epochs), accuracy)
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.suptitle("Accuracy per epoch")
    plt.show()
