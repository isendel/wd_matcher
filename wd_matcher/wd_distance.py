import Levenshtein


class WDDistance:
    @staticmethod
    def get_distance(string1, string2):
        return Levenshtein.distance(string1.lower(), string2.lower())

    @staticmethod
    def get_scaled_distance(string1, string2):
        scale = len(string1) + len(string2)
        if scale != 0:
            return Levenshtein.distance(string1.lower(), string2.lower()) / scale
        else:
            return 0

    @staticmethod
    def get_scaled_distance_array(array1, array2):
        if len(array1) == 0 or len(array2) == 0:
            raise Exception('Arrays shouldn\'t be empty.')
        if len(array1) != len(array2):
            raise Exception('Array length are not equal.')
        result_ = []
        for val1, val2 in zip(array1, array2):
            result_.append(WDDistance.get_scaled_distance(val1, val2))
        return result_
