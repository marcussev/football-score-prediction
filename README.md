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
1. Run dataprocessor.py to download and process the data to be used:
```bash
cd data
python3 dataprocessor.py
```
2. Run test files in ./test to train and evauluate models:
```bash
cd tests
python3 enter_file_name_here.py
```
3. Tranied models are saved to ./results/trained_models
4. Graphs displaying accuracy and loss are saved to ./results/graphs
5. Full match predictions is also saved to ./results

## Predcit future results
In this project the linear regression model achieved the best results gived the data and features at hand. To predict any football game using this model, you can run the ./main:
```bash
python3 main.py
```
You will be prompted to enter each revelant game statistic and the program will the give you its prediction
