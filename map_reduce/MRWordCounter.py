from mrjob.job import MRJob

class MRWordCounter(MRJob):
    def mapper(self, key, document):
        for word in document.split():
            yield word, 1
    def reducer(self, word, occurrences):
        yield word, sum(occurrences)
MRWordCounter.run()