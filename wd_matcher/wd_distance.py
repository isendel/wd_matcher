import Levenshtein


class WDDistance:
    @staticmethod
    def get_distance(string1, string2):
        return Levenshtein.distance(string1, string2)
