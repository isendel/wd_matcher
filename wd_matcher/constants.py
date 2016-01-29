import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

WORKS_DATASET_FILE = 'dataset/' + config['GEN']['environment'] + '_works_dataset.csv'
WORKS_DISTANCE_DATASET_FILE = 'dataset/' + config['GEN']['environment'] + '_works_distance_dataset.csv'
