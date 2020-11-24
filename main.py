from data import dataprocessor
from utils import save_as_csv
from tests import feature_selection

# --------------------------------------------------------------------------------
# This file can be ran to initialize datasets and perform feature analysis
# --------------------------------------------------------------------------------

if __name__ == '__main__':

    # Preprocess raw data to desired format
    interim = dataprocessor.process_raw_data()
    save_as_csv(interim, 'data/datasets/interim/game_stats.csv')

    # Create datasets with simple game statistics
    simple_train_data, simple_test_data = dataprocessor.get_simplified_data(interim)
    save_as_csv(simple_train_data, 'data/datasets/processed/simple_train_data.csv')
    save_as_csv(simple_test_data, 'data/datasets/processed/simple_test_data.csv')

    # Create datasets with advanced game statistics
    adv_train_data, adv_test_data, full_data = dataprocessor.get_advanced_data(interim)
    save_as_csv(adv_train_data, 'data/datasets/processed/adv_train_data.csv')
    save_as_csv(adv_test_data, 'data/datasets/processed/adv_test_data.csv')
    save_as_csv(full_data, 'data/datasets/processed/full_data.csv')

    # Analyze feature importance
    # If you want to select different features for your optimized models based on the analysis,
    # you have to change them manually in dataprocessor.py
    feature_selection.get_regression_importance(full_data)
    feature_selection.get_mlp_importance(full_data)

    # Create datasets with optimal features based on observed feature importance
    opt_reg_train, opt_reg_test = dataprocessor.get_optimal_reg_data(interim)
    save_as_csv(opt_reg_train, 'data/datasets/processed/opt_reg_train.csv')
    save_as_csv(opt_reg_test, 'data/datasets/processed/opt_reg_test.csv')

    opt_mlp_train, opt_mlp_test = dataprocessor.get_optimal_mlp_data(interim)
    save_as_csv(opt_mlp_train, 'data/datasets/processed/opt_mlp_train.csv')
    save_as_csv(opt_mlp_test, 'data/datasets/processed/opt_mlp_test.csv')