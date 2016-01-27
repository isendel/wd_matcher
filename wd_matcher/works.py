class WordDocument:
    def __init__(self, work):
        self.work = work

    def get_document_features(self):
        features = {
            'publisher.publisher_name':
                self.get_work_item_value(self.work, 'work▪publisher.work▪publisher▪name.val'),
            'publisher.place_of_publication':
                self.get_work_item_value(self.work, 'work▪publisher.work▪publisher▪placeOfPublication.val'),
            'publication_type':
                self.get_work_item_value(self.work, 'work▪publicationType.val'),
            'country_of_publication':
                self.get_work_item_value(self.work, 'work▪publicationCountry.work▪publicationCountry▪country.val'),
            'language':
                self.get_work_item_value(self.work, 'work▪workLanguage.work▪workLanguage▪language.val'),
            'contributor.name':
                self.get_work_item_value(self.work, 'work▪contributor.work▪contributor▪contributorName.val'),
            'contributor.role':
                self.get_work_item_value(self.work, 'work▪contributor.work▪contributor▪contributorRole.val'),
            'title':
                self.get_work_item_value(self.work, 'work▪workTitle.work▪workTitle▪title.val'),
            'idno':
                self.get_work_item_value(self.work, 'work▪idno.work▪idno▪idno.val'),
            'idno.type':
                self.get_work_item_value(self.work, 'work▪idno.work▪idno▪type.val'),
            'subject':
                self.get_work_item_value(self.work, 'work▪workSubject.work▪workSubject▪subject.val'),
            'publishing_work_items.value':
                self.get_work_item_value(self.work, 'work▪extent.work▪extent▪extentValueRaw.val'),
            'publishing_work_items.type':
                self.get_work_item_value(self.work, 'work▪extent.work▪extent▪extentType.val'),
            'publishing_work_items.unit':
                self.get_work_item_value(self.work, 'work▪extent.work▪extent▪extentUnit.val')
        }

        return features

    def get_work_item_value(self, work, path):
        path_array = path.split('.')
        if len(path_array) == 0 or '' == path:
            return work
        if 'work' in work and 'workItemValues' in work['work']:
            return self.get_work_item_value(work['work']['workItemValues'], path)
        elif type(work) == list:
            result = ''
            for list_item in work:
                value = self.get_work_item_value(list_item, path)
                if '' != value:
                    result = '%s %s' % (result, value)
            return result.strip()
        elif type(work == dict):
            if path_array[0] in work:
                return self.get_work_item_value(work[path_array[0]], '.'.join(path_array[1:]))
            elif 'items' in work:
                return self.get_work_item_value(work['items'], '.'.join(path_array))
        return ''
