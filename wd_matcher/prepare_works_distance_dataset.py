import configparser
import csv
import logging
from wd_matcher.wd_distance import WDDistance
from wd_matcher.constants import WORKS_DATASET_FILE
from wd_matcher.constants import WORKS_DISTANCE_DATASET_FILE
from wd_matcher.constants import WORKS_DISTANCE_DATASET_CMP_FILE
from wd_matcher.works import document_fields

logger = logging.getLogger('prepare_dataset')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

config = configparser.ConfigParser()
config.read('settings.ini')

max_rows = -1
match_strategy = {'publication_type': 'simple_match',
                  'contributor.role': 'simple_match',
                  'idno.type': 'simple_match'}


def generate_dataset():
    with open(WORKS_DISTANCE_DATASET_CMP_FILE, 'w', encoding='utf8') as works_distance_dataset_file_augm:
        with open(WORKS_DISTANCE_DATASET_FILE, 'w', encoding='utf8') as works_distance_dataset_file:
            works_distance_dataset = csv.writer(works_distance_dataset_file, lineterminator='\n')
            works_distance_dataset_augm = csv.writer(works_distance_dataset_file_augm, lineterminator='\n')
            with open(WORKS_DATASET_FILE, 'r', encoding='utf-8') as works_dataset_file:
                works_dataset = csv.reader(works_dataset_file)
                current_row = 0
                row1 = None
                for row in works_dataset:
                    if current_row % 500 == 0:
                        print('Processed %s rows' % current_row)
                    if current_row == 0:
                        works_distance_dataset.writerow(row)
                        works_distance_dataset_augm.writerow(row)
                        row = next(works_dataset)
                    if current_row % 2 == 0:
                        row1 = row
                    else:
                        distance_array = WDDistance.get_scaled_distance_array(
                                row1[:len(row) - 1], row[:len(row) - 1], document_fields, match_strategy)
                        works_distance_dataset_augm.writerow(row1[:len(row) - 1])
                        works_distance_dataset_augm.writerow(row[:len(row) - 1])
                        works_distance_dataset_augm.writerow(
                                distance_array + [
                                    row[len(row) - 1]])
                        works_distance_dataset.writerow(
                                distance_array + [
                                    row[len(row) - 1]])
                    current_row += 1
                    if max_rows != -1 and current_row >= max_rows:
                        break


generate_dataset()
