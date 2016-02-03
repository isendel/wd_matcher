import Levenshtein
from fuzzywuzzy import fuzz


class WDDistance:
    @staticmethod
    def get_fuzzy_distance(string1, string2):
        # if (len(string1) == 0 or len(string2) == 0) and len(string1) + len(string2) != 0:
        if len(string1) == 0 or len(string2) == 0:
            return 0
        if '|' in string1:
            string1 = ' '.join(string1.split('|'))
        if '|' in string2:
            string2 = ' '.join(string2.split('|'))
        return fuzz.token_sort_ratio(string1, string2)

    @staticmethod
    def get_simple_distance(string1, string2):
        # if '|' in string1:
        set1 = set(string1.split('|'))
        # if '|' in string2:
        set2 = set(string2.split('|'))
        intersection = set1 & set2
        if len(intersection) == 0:
            return 0
        else:
            return ((len(intersection)) * 100) / (max([len(set1), len(set2)]))

    @staticmethod
    def get_distance(string1, string2, strategy):
        if 'simple_match' == strategy:
            return WDDistance.get_simple_distance(string1, string2)
        else:
            return WDDistance.get_fuzzy_distance(string1, string2)

    @staticmethod
    def get_scaled_distance_array(array1, array2, columns, match_strategy):
        if len(array1) == 0 or len(array2) == 0:
            raise Exception('Arrays shouldn\'t be empty.')
        if len(array1) != len(array2):
            raise Exception('Array length are not equal.')
        result_ = []
        field_count = 0
        for val1, val2 in zip(array1, array2):
            current_field = columns[field_count]
            if current_field in match_strategy:
                result_.append(WDDistance.get_distance(val1, val2, match_strategy[current_field]))
            else:
                result_.append(WDDistance.get_distance(val1, val2, 'default'))
            field_count += 1
        return result_
