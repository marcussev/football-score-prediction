# football-score-prediction
This is a machine learning project I did as a research assignment for the course "TDAT3025 Applied Machine Learning with project" at NTNU. The aim was to predict future football results with various machine learning techniques based on statistics from previuos games.

## Install Dependencies
The following packages needs to be installed to reproduce this project:

1. Python
2. Matplotlib
3. Numpy
4. Pandas
5. Scikit-learn
6. torch

You should be able to quickly install all requirements by running the following line in your terminal/console:
```bash
pip3 install -r requirements.txt
```
If this does not work try installing each package individually.

## Get started
To reproduce the analysis and research results, do the following steps:
1. Make sure the raw dataset is downloaded to ./data/datasets/raw/ from https://www.kaggle.com/idoyo92/epl-stats-20192020. 
Then run main.py to preprocess and do feature analysis of the data:
    ```bash
    python3 main.py
    ```
2. After all datasets are saved, run test files in ./test to train and evaluate models:
    ```bash
    cd tests/folder_name_here
    python3 file_name_here.py
    ```
3. If you want to save graphs from the tests, make sure to uncomment plt.savefig()
in visualizer.py methods.

