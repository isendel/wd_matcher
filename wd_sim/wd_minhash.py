import os
import psutil
from nltk.util import ngrams
from datasketch.lsh import LSH
from datasketch.minhash import MinHash
from hashlib import sha1
from uuid import uuid4
import timeit
import pickle

metadata_fields = []
for i in range(20):
    metadata_fields.append('field_name_%s' % i)


def create_object():
    """
    Creates a dummy dict object that has as many keys as the length of metadata_fields objects and
    UUIDs as values for them.
    :return a constructed dummy dict:
    """
    obj_ = {}
    for f_ in metadata_fields:
        obj_[f_] = str(uuid4())
    return obj_


def my_tokenizer(word_document):
    """
    Tokenize dict into namespaced ngrams
    :param word_document: dictionary object
    :return a set of tokens:
    """
    tokens_ = set()
    for key, value in word_document.items():
        grams_ = ngrams(value, 3)
        for gram in [('%s=%s' % (key, ''.join(x))).lower() for x in grams_]:
            tokens_.add(gram)
    return tokens_


def dict_to_minhash(v):
    """
    Generates a Minhash for a dict object
    :param v: dictionary
    :return: minhash
    """
    m_ = MinHash()
    tokens = my_tokenizer(v)
    for t in tokens:
        m_.digest(sha1(t.encode('utf8')))
    return m_


def main_minhash():
    f = open('dataset/minhashes.bin', 'wb')
    process = psutil.Process(os.getpid())
    counter = 0
    size = 0
    for _ in range(10000):
        obj_ = create_object()
        m = dict_to_minhash(obj_)
        pickle.dump(m, f)
        counter += 1
        # lsh.insert('#%s' % counter, m)
        size += m.bytesize()
        if counter % 100 == 0:
            print('%s objects minhashed. Total size: %s bytes' % (counter, size))
            print('Memory consumed: %s bytes.' % process.memory_info().rss)
    f.close()


def main_lhs_insert():
    f = open('dataset/minhashes.bin', 'rb')
    m = pickle.load(f)
    counter = 0
    lsh = LSH(threshold=0.2, num_perm=128)
    while m is not None:
        counter += 1
        lsh.insert('#%s' % counter, m)
        if counter % 100 == 0:
            print('%s minhashes loaded.' % counter)
        try:
            m = pickle.load(f)
        except EOFError:
            print('End loading minhashes.')
            break


# print(timeit.timeit(main, number=1))
# obj = create_object()
# m = dict_to_minhash(obj)
# print(m.bytesize())

main_minhash()
# main_lhs_insert()
