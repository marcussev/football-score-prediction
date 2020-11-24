import visualizer

# --------------------------------------------------------------------------------
# This file plots observed accuracies from all the different models in a bar chart
# --------------------------------------------------------------------------------

if __name__ == '__main__':
    accuracies = [57.25, 56.72, 52.25, 52.25, 52.25, 55.22, 45.00, 53.00]
    models = ["Avansert Regresjon", "Simpel Regresjon", "Optimalisert Regresjon",
              "Avansert MLP", "Simpel MLP", "Optimalisert MLP", "Random Forest", "Bookmakere"]
    visualizer.plot_comparison(accuracies, models, "../results/graphs/model_comparison.png")
