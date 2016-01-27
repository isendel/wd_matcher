import csv
import json
import configparser
import os
import shutil

from pymongo import MongoClient
from wd_matcher.works import WordDocument

config = configparser.ConfigParser()
config.read('settings.ini')

max_rel = 10
client = MongoClient(config['DEV']['mongodb.host'], int(config['DEV']['mongodb.port']))
db = client.works
works_collection = db.archive_works


def get_work_rel_row_info(rel):
    print(rel)
    relation_ = rel['storageEquivalenceRelation']
    representative_work_id_ = relation_['representativeWorkId']
    incoming_work_id_ = relation_['incomingWorkId']
    print(get_work(incoming_work_id_))
    print(get_work(representative_work_id_))
    return (WordDocument(get_work(incoming_work_id_))), (WordDocument(get_work(representative_work_id_)))


def get_work(work_id):
    return works_collection.find_one({'_id': work_id})


def dump_rel_to_csv(filter):
    with open('documents_rel.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile, lineterminator='\n')
        equivalence_relations = db.equivalence_relations
        rel_processed = 0
        equivalence_relations_cursor = equivalence_relations.find(
                {"storageEquivalenceRelation.equivalenceRelation.equivalenceType": filter})
        for rel in equivalence_relations_cursor:
            relation_ = rel['storageEquivalenceRelation']
            try:
                incoming_work_id = relation_['incomingWorkId']
                representative_work_id = relation_['representativeWorkId']
            except KeyError as e:
                print('Error occurred...')
                print(e)
            else:
                work_incoming = works_collection.find_one({'_id': incoming_work_id})
                work_representative = works_collection.find_one({'_id': representative_work_id})
                if work_incoming and work_representative:
                    if rel_processed >= max_rel:
                        break
                    else:
                        rel_processed += 1
                    # work_info = get_work_info(work_incoming, work_representative)
                    work1, work2 = get_work_rel_row_info(rel)
                    label = relation_['equivalenceRelation']['equivalenceType']
                    with open('dataset/%s_document_%s_1.json' % (label, rel_processed), 'w') as work1_file:
                        json.dump(work1.get_document_features(), work1_file)
                    with open('dataset/%s_document_%s_2.json' % (label, rel_processed), 'w') as work2_file:
                        json.dump(work2.get_document_features(), work2_file)
        print('%s/%s relationships are valid' % (rel_processed, max_rel))


if os.path.exists('dataset'):
    shutil.rmtree('dataset')
os.makedirs('dataset')
dump_rel_to_csv('FORCE_MATCH')
dump_rel_to_csv('FORCE_NO_MATCH')
