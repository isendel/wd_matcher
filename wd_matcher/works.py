document_fields = [
    'publisher.publisher_name',
    'publisher.place_of_publication',
    'publication_type',
    'country_of_publication',
    'language',
    'contributor.name',
    'contributor.role',
    'title',
    'idno',
    'idno.type',
    'subject',
    'publishing_work_items.value',
    'publishing_work_items.type',
    'publishing_work_items.unit',
    'primary_author',
]


class WordDocument:
    def __init__(self, work):
        self.work = work

    def get_features_array(self):
        result = []
        features = self.get_document_features()
        for field in document_fields:
            result.append(features[field])
        return result

    def get_document_features(self):
        features = {
            document_fields[0]:
                self.get_work_item_value(self.work, 'work▪publisher.work▪publisher▪name.val'),
            document_fields[1]:
                self.get_work_item_value(self.work, 'work▪publisher.work▪publisher▪placeOfPublication.val'),
            document_fields[2]:
                self.get_work_item_value(self.work, 'work▪publicationType.val'),
            document_fields[3]:
                self.get_work_item_value(self.work, 'work▪publicationCountry.work▪publicationCountry▪country.val'),
            document_fields[4]:
                self.get_work_item_value(self.work, 'work▪workLanguage.work▪workLanguage▪language.val'),
            document_fields[5]:
                self.get_work_item_value(self.work, 'work▪contributor.work▪contributor▪contributorName.val'),
            document_fields[6]:
                self.get_work_item_value(self.work, 'work▪contributor.work▪contributor▪contributorRole.val'),
            document_fields[7]:
                self.get_work_item_value_filtered(self.work, 'work▪workTitle.work▪workTitle▪title#$1.val',
                                                  'work▪workTitle.work▪workTitle▪type.val=MAIN'),
            document_fields[8]:
                self.get_work_item_value(self.work, 'work▪idno.work▪idno▪idno.val'),
            document_fields[9]:
                self.get_work_item_value(self.work, 'work▪idno.work▪idno▪type.val'),
            document_fields[10]:
                self.get_work_item_value(self.work, 'work▪workSubject.work▪workSubject▪subject.val'),
            document_fields[11]:
                self.get_work_item_value(self.work, 'work▪extent.work▪extent▪extentValueRaw.val'),
            document_fields[12]:
                self.get_work_item_value(self.work, 'work▪extent.work▪extent▪extentType.val'),
            document_fields[13]:
                self.get_work_item_value(self.work, 'work▪extent.work▪extent▪extentUnit.val'),
            document_fields[14]:
                self.get_work_item_value(self.work, 'work▪contributor.work▪contributor▪contributorName.val',
                                         'work▪contributor.work▪contributor▪contributorRole=2'),
        }

        return features

    def get_work_item_value_filtered(self, work, path, filter):
        filter_split = filter.split('=')
        value = self.get_work_item_value(work, filter_split[0], '__').split('__')
        value_indexes = [str(i) for i, x in enumerate(value) if x == filter_split[1]]
        return self.get_work_item_value(work, path.replace('$1', '|'.join(value_indexes)))

    def get_work_item_value(self, work, path, list_separator='|'):
        path_array = path.split('.')
        if len(path_array) == 0 or '' == path:
            return work
        filter_index = []
        current_path_item = path_array[0]
        if '#' in current_path_item:
            filter_index = current_path_item.split('#')[1].split('|')
            current_path_item = current_path_item.split('#')[0]
        if 'work' in work and 'workItemValues' in work['work']:
            return self.get_work_item_value(work['work']['workItemValues'], path, list_separator)
        elif type(work) == list:
            results = []
            for i, list_item in enumerate(work):
                if len(filter_index) == 0 or str(i) in filter_index:
                    value = self.get_work_item_value(list_item, path, list_separator)
                    if '' != value:
                        results.append(value.strip())
            return list_separator.join(results)
        elif type(work == dict):
            if current_path_item in work:
                return self.get_work_item_value(work[current_path_item], '.'.join(path_array[1:]), list_separator)
            elif 'items' in work:
                return self.get_work_item_value(work['items'], '.'.join(path_array), list_separator)
        return ''
