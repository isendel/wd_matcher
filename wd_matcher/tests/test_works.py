import unittest
import json
from wd_matcher.works import WordDocument


class WordDocumentFeatureDistancesTestCase(unittest.TestCase):
    def setUp(self):
        with open('works_data/work_data.json', 'rb') as data_file:
            data = data_file.read()
        self.work = json.loads(data.decode('utf-8'))
        self.wordDocumentDistances = WordDocument(self.work)

    def test_get_work_item_value(self):
        self.assertEqual('Nature Publishing Group'.lower(),
                         self.wordDocumentDistances.get_work_item_value(self.work,
                                                                        'work▪publisher.work▪publisher▪name.val').lower())
        self.assertEqual('New York, NY'.lower(),
                         self.wordDocumentDistances.
                         get_work_item_value(self.work,
                                             'work▪publisher.work▪publisher▪placeOfPublication.val').lower())

        self.assertEqual('USA'.lower(),
                         self.wordDocumentDistances.
                         get_work_item_value(self.work,
                                             'work▪publicationCountry.work▪publicationCountry▪country.val').lower())

    def test_get_root_st(self):
        self.assertEqual('10', self.wordDocumentDistances.get_work_item_value(self.work, 'work▪publicationType.val'))

    def test_get_work_item_value_multy(self):
        value = self.wordDocumentDistances.get_work_item_value(self.work,
                                                               'work▪contributor.'
                                                               'work▪contributor▪contributorName.val').lower()
        self.assertEqual('AMERICAN THERAPEUTIC SOCIETY.|AMERICAN SOCIETY FOR CLINICAL PHARMACOLOGY AND THE|'
                         'AMERICAN SOCIETY FOR PHARMACOLOGY AND EXPERIMENTAL|STEIN, C. MICHAEL'.lower(),
                         value)

    def test_get_work_item_value_by_order_number(self):
        value = self.wordDocumentDistances.get_work_item_value_filtered(self.work,
                                                                        'work▪workTitle.work▪workTitle▪title#$1.val',
                                                                        'work▪workTitle.work▪workTitle▪type.val=MAIN')
        self.assertEqual('Clinical pharmacology and therapeutics'.lower(), value.lower())

    def test_get_author(self):
        value = self.wordDocumentDistances.get_work_item_value_filtered(self.work,
                                                                        'work▪contributor.work▪contributor▪contributorName#$1.val',
                                                                        'work▪contributor.work▪contributor▪contributorRole.val=2')
        self.assertEqual('AMERICAN THERAPEUTIC SOCIETY.|'
                         'AMERICAN SOCIETY FOR CLINICAL PHARMACOLOGY AND THE|'
                         'AMERICAN SOCIETY FOR PHARMACOLOGY AND EXPERIMENTAL', value)
