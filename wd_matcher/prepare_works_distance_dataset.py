import configparser
import csv
import logging
from wd_matcher.wd_distance import WDDistance
from wd_matcher.constants import WORKS_DATASET_FILE
from wd_matcher.constants import WORKS_DISTANCE_DATASET_FILE

logger = logging.getLogger('prepare_dataset')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

config = configparser.ConfigParser()
config.read('settings.ini')

def generate_dataset():
    with open(WORKS_DISTANCE_DATASET_FILE, 'w') as works_distance_dataset_file:
        works_distance_dataset = csv.writer(works_distance_dataset_file, lineterminator='\n')
        with open(WORKS_DATASET_FILE, 'r') as works_dataset_file:
            works_dataset = csv.reader(works_dataset_file)
            current_row = 0
            row1 = None
            for row in works_dataset:
                if current_row == 0:
                    works_distance_dataset.writerow(row)
                    next(works_dataset)
                if current_row % 2 == 0:
                    row1 = row
                else:
                    distance_array = WDDistance.get_scaled_distance_array(row1[:len(row)-1], row[:len(row)-1])
                    works_distance_dataset.writerow(
                            distance_array + [
                                row[len(row) - 1]])
                current_row += 1


generate_dataset()
