from mrjob.job import MRJob

class number_sum(MRJob):
	def mapper(self, key, document):
		for word in document.split(','):
			yield "_", float(word)

	def reducer(self, word, occurrences):
		yield word, sum(occurrences)

number_sum.run()