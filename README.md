# football-score-prediction

This is a machine learning project aiming to predict outcomes of football games, based on each teams underlying stats. It consists of tools for datascraping, model training, and an API to interact with the predictor.

## Tech stack

- **Datascraping**: _BeautifulSoup_
- **Data processing**: _Pandas and Numpy_
- **Feature validation**: _Scikit-learn_
- **Model training**: _PyTorch_
- **API**: _Flask_
- **Database**: _Cloud Firestore_

## Project status

The project is still under development, and there are several planned improvements and future features to be implemented. Model performance and accuracy is currently estimated on a relatively small dataset (~280 games) and results should therefore be taken with a pinch of salt..

### Current features

- Data and predictions for multiple leagues (English Premier League, Bundesliga, La Liga)
- A firestore database for storing underlying data and predictions
- Tools for scraping both training data and keeping stats up to date
- Multiple approaches to predictions
  1.  Linear Regression for predicting each teams number of goals
  2.  MLP Neural Network for predicting winner (Home, away or draw)
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
