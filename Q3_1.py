# This class implements the "Most Likely Tag" baseline
class MostLikelyTagEstimator:
	# The constructor accepts an optional file name
	# for the training set of tagged sentences
	def __init__(self, trainingFileName = 'pos_tagged.txt'):
		# The tagset will be stored as a set
		self._tagSet = set()

		# Each word and its most likely tag
		# will be stored as a key/value pair
		# in a dictionary
		self._mostLikelyTags = dict()

		# Each word and its p*(t|w) value
		# will be stored as a key/value pair
		# in a dictionary
		self._mostLikelyProbabilities = {}

		# The tokenized training set will
		# be stored in a list
		self._trainingCorpus = []

		# Train our tagger on the
		# provided training set
		self.Train(trainingFileName)

	# Train the tagger on the training set
	# trainingFileName is the name of the file containing
	# the training set of tagged sentences
	def Train(self, trainingFileName = 'pos_tagged.txt'):
		try:
			# Tokenize the training set text file by splitting
			# on whitespace first, then for each element in
			# the list, we split on '/'.
			# This results in a list of lists, of the form
			# [[word1, tag1], [word2, tag2], ...]
			# (note that the file closes automatically)
			with open(trainingFileName) as trainingFile:
				self._trainingCorpus = list(x.split('/') for x in trainingFile.read().split())
		except IOError:
			print(f'Error: Could not open {trainingFileName}')
			print('Call \'Train(FileName)\' to read the correct file.')
		else:
			# Extract the tagset and words from this corpus
			for wordTagPair in self._trainingCorpus:
				# Initialize each word's p*(t|w) value to 0
				self._mostLikelyProbabilities[wordTagPair[0]] = 0
				# Initialize each word's most likely tag to ""
				self._mostLikelyTags[wordTagPair[0]] = ""
				# Populate the tagset
				self._tagSet.add(wordTagPair[1])

			# We'll need this in a few places below
			trainingCorpusLength = len(self._trainingCorpus)

			# Print the progress bar
			self._printProgressBar(0, trainingCorpusLength)
			# Calculate the most likely tag and p*(t|w) value for each word
			for i in range(trainingCorpusLength):
				word = self._trainingCorpus[i][0]

				# Previous Tag is empty if we are at the beginning
				previousTag = self._trainingCorpus[i - 1][1] if i != 0 else ""
				currentTag = self._trainingCorpus[i][1]

				# approximate p*(t|w) by (C(tag, previousTag)/C(tag)))*(C(tag, word)/C(tag))
				highestProbability = self._calculatePriorTimesLikelihood(currentTag, previousTag, word)
				if highestProbability > self._mostLikelyProbabilities[word]:
					# Assign new highest p*(t|w) value to word
					self._mostLikelyProbabilities[word] = highestProbability

					# Assign new tag to word
					self._mostLikelyTags[word] = currentTag

				# Update the progress bar
				self._printProgressBar(i + 1, trainingCorpusLength)

	# Print each word's p*(t|w) value and most likely tag in a neat table
	def PrintProbabilities(self):
		print("-" * 100)
		print(f"{'Word':<40s}| {'p*(t|w)':<25s}| {'Most Likely Tag':<10s}")
		print("-" * 100)
		for word in self._mostLikelyProbabilities:
			print(f"{word:<40s}| {str(self._mostLikelyProbabilities[word]):<25s}| {str(self._mostLikelyTags[word]):<10s}")

	# Helper method to calculate p*(t|w) = Prior * Likelihood
	# = (C(tag, previousTag)/C(tag)))*(C(tag, word)/C(tag))
	def _calculatePriorTimesLikelihood(self, currentTag, previousTag, word):
		# C(tag, previousTag)
		numCombinedPrior = 0

		# C(tag, word)
		numCombinedLikelihood = 0

		# C(tag)
		numOccurrences = 0

		if previousTag == "":
			# word is the first word in the corpus,
			# so we only calculate 1 * Likelihood
			for wordTagPair in self._trainingCorpus:
				if wordTagPair[1] == currentTag:
					numOccurrences += 1
					if wordTagPair[0] == word:
						numCombinedLikelihood += 1
			
			return numCombinedLikelihood / numOccurrences
		else:
			# Otherwise, we calculate Prior * Likelihood

			# First, handle the special case for the first word
			# with no previous tag
			if self._trainingCorpus[0][1] == currentTag:
				numOccurrences += 1

			# Next, tally the counts necessary to calculate
			# Prior * Likelihood
			for i in range(len(self._trainingCorpus) - 1):
				if self._trainingCorpus[i + 1][1] == currentTag:
					numOccurrences += 1
					if self._trainingCorpus[i][1] == previousTag:
						numCombinedPrior += 1
					if self._trainingCorpus[i + 1][0] == word:
						numCombinedLikelihood += 1
			
			return (numCombinedPrior / numOccurrences) * (numCombinedLikelihood / numOccurrences)


	# Training the tagger takes some time for large corpora, so we'll need to implement a simple progress bar
	def _printProgressBar(self, currentIteration, totalIterations, precision = 1, width = 60, fillChar = '='):
		percentageComplete = ("{0:." + str(precision) + "f}").format(100 * (currentIteration / float(totalIterations)))
		filledLength = int(width * currentIteration // totalIterations)
		toPrint = fillChar * filledLength + '.' * (width - filledLength)
		print(f'\r{"Training in progress:"} [{toPrint}] {percentageComplete}% {"Complete"}', end = "\r")
		# Print newlines once complete
		if currentIteration == totalIterations: 
			print()
			print()

def main():
	print("----------------------------------------------------------------------------------------------------")
	print("This program computes p*(t|w) = argmax p(t|w) for each word in a provided corpus of tagged sentences")
	print("----------------------------------------------------------------------------------------------------\n")

	# Instantiate our estimator
	mle = MostLikelyTagEstimator()

	# Print the computed probabilities
	mle.PrintProbabilities()

	# Wait for input to continue
	input("\nPress <RETURN> to continue")

if __name__ == "__main__":
	print("\n===============================================")
	print("62760858 - COS4861 - Assignment 2 - 2021 - Q3_1")
	print("===============================================\n")
	main()