import csv
import configparser
import os
import logging
import shutil
from pymongo import MongoClient
from wd_matcher.works import WordDocument
from wd_matcher.works import document_fields
from wd_matcher.constants import WORKS_DATASET_FILE

logger = logging.getLogger('prepare_dataset')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

config = configparser.ConfigParser()
config.read('settings.ini')

max_rel = -1
client = MongoClient(config['GEN']['mongodb.host'], int(config['GEN']['mongodb.port']))
db = client.works
works_collection = db.archive_works


def get_work_rel_row_info(rel):
    relation_ = rel['storageEquivalenceRelation']
    representative_work_id_ = relation_['representativeWorkId']
    incoming_work_id_ = relation_['incomingWorkId']
    return (WordDocument(get_work(incoming_work_id_))), (WordDocument(get_work(representative_work_id_)))


def get_work(work_id):
    return works_collection.find_one({'_id': work_id})


def dump_rel_to_csv(filters):
    with open(WORKS_DATASET_FILE, 'w', encoding='utf8') as csvfile:
        csv_writer = csv.writer(csvfile, lineterminator='\n')
        csv_writer.writerow(document_fields + ['label'])
        equivalence_relations = db.equivalence_relations
        for filter in filters:
            equivalence_relations_cursor = equivalence_relations.find(
                    {'storageEquivalenceRelation.equivalenceRelation.equivalenceType': filter})
            rel_processed = 0
            for rel in equivalence_relations_cursor:
                relation_ = rel['storageEquivalenceRelation']
                try:
                    incoming_work_id = relation_['incomingWorkId']
                    representative_work_id = relation_['representativeWorkId']
                except KeyError as e:
                    logger.error('Error occurred...')
                    logger.error(e)
                else:
                    work_incoming = works_collection.find_one({'_id': incoming_work_id})
                    work_representative = works_collection.find_one({'_id': representative_work_id})
                    if work_incoming and work_representative:
                        if max_rel != -1 and rel_processed >= max_rel:
                            break
                        else:
                            rel_processed += 1
                        work1, work2 = get_work_rel_row_info(rel)
                        label = 0
                        if relation_['equivalenceRelation']['equivalenceType'] == 'FORCE_MATCH':
                            label = 1
                        csv_writer.writerow(work1.get_features_array() + [label])
                        csv_writer.writerow(work2.get_features_array() + [label])
                        if rel_processed % 100 == 0:
                            logger.info('Relationships processed %s/%s for %s' % (rel_processed, max_rel, filter))
            logger.info('%s/%s relationships are valid for filter %s' % (rel_processed, max_rel, filter))


if os.path.exists('dataset'):
    shutil.rmtree('dataset')
os.makedirs('dataset')
dump_rel_to_csv(['FORCE_NO_MATCH', 'FORCE_MATCH'])
# dump_rel_to_csv('FORCE_MATCH')
# dump_rel_to_csv('FORCE_NO_MATCH')
