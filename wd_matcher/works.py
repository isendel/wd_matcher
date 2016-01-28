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
    'publishing_work_items.unit'
]


class WordDocument:
    def __init__(self, work):
        self.work = work

    def get_features_array(self):
        result = []
        features = self.get_document_features()
        for field in document_fields:
            result.append(features[field].encode('utf-8'))
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
                self.get_work_item_value(self.work, 'work▪extent.work▪extent▪extentUnit.val')
        }

        return features

    def get_work_item_value_filtered(self, work, path, filter):
        filter_split = filter.split('=')
        value = self.get_work_item_value(work, filter_split[0], '%s__%s').split('__')
        return self.get_work_item_value(work, path.replace('$1', str(value.index(filter_split[1]))))

    def get_work_item_value(self, work, path, list_formatter='%s %s'):
        path_array = path.split('.')
        if len(path_array) == 0 or '' == path:
            return work
        filter_index = -1
        current_path_item = path_array[0]
        if '#' in current_path_item:
            filter_index = int(current_path_item.split('#')[1])
            current_path_item = current_path_item.split('#')[0]
        if 'work' in work and 'workItemValues' in work['work']:
            return self.get_work_item_value(work['work']['workItemValues'], path, list_formatter)
        elif type(work) == list:
            result = ''
            for i, list_item in enumerate(work):
                if filter_index == i or filter_index == -1:
                    value = self.get_work_item_value(list_item, path, list_formatter)
                    if '' != value:
                        if result == '':
                            result = value
                        else:
                            result = list_formatter % (result, value)
            return result.strip()
        elif type(work == dict):
            if current_path_item in work:
                return self.get_work_item_value(work[current_path_item], '.'.join(path_array[1:]), list_formatter)
            elif 'items' in work:
                return self.get_work_item_value(work['items'], '.'.join(path_array), list_formatter)
        return ''
