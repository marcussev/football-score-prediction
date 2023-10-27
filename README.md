# football-score-prediction
This is a machine learning project aiming to predict outcomes of football games, based on each teams underlying stats. It consists of tools for datascraping, model training, and an API to interact with the predictor.

## Tech stack
- **Datascraping**: *BeautifulSoup*
- **Data processing**: *Pandas and Numpy*
- **Feature validation**: *Scikit-learn*
- **Model training**: *PyTorch*
- **API**: *Flask*
- **Database**: *Cloud Firestore*

## Project status
The project is still under development, and there are several planned improvements and future features to be implemented. Model performance and accuracy is currently estimated on a relatively small dataset (~280 games) and results should therefore be taken with a pinch of salt..

### Current features
- Data and predictions for multiple leagues (English Premier League, Bundesliga, La Liga)
- A firestore database for storing underlying data and predictions
- Tools for scraping both training data and keeping stats up to date
- Multiple approaches to predictions
   1. Linear Regression for predicting each teams number of goals
   2. MLP Neural Network for predicting winner (Home, away or draw)
- An API for interacting with the data and predictions
- Tools for visualizing model performance and accuracy

### Current performance
- Linear Regression: ~52-58% accuracy (Depending on number of input features)
- MLP Neural Network: ~50-55% accuracy (Depending on number of input features)

#### Benchmarks
- Random: 33,3%
- Bookmakers: ~50-55%

### To do
- Automate scraping and predictions with cron jobs
- Implement logging system for all changes performed on data and predictions
- Increase amount of training data and hopefully accuracy
- Create a command line interface to interact with API

## Steps to reproduce

### Install dependencies

```bash
python -m venv <your-env>
.\<your-env>\Scripts\activate
pip install -r requirements.txt
```

### Setup a Cloud Firestore database
Follow the steps from Firebase official documentation to setup your own Firestore database:
[Python Client for Cloud Firestore API](https://cloud.google.com/python/docs/reference/firestore/latest)

Add your certificate file as db-key.json at in the following directory:
```
<PATH_TO_ROOT>/api/db/<db-key.json>
```

### Quick test if models
To reproduce quickly reproduce an analysis and some test results, do the following steps:
1. Make sure you have raw dataset saved to ```<PATH_TO_ROOT>/data/datasets/raw/```. For quick testing you can use the data from https://www.kaggle.com/idoyo92/epl-stats-20192020. 
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

### Scrape for training data
Scraping for training data can be done both from the API and by running a script.

