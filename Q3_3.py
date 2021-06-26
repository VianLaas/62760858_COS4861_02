from Q3_1 import MostLikelyTagEstimator
import webbrowser

class MostLikelyTagAnalyzer(MostLikelyTagEstimator):
	def __init__(self, trainingFileName = 'pos_tagged.txt', goldenFileName = 'pos_golden_standard.txt'):
		super().__init__(trainingFileName)

		# The Confusion Matrix will
		# be stored as a nested dictionary
		self._confusionMatrix = dict()

		# The tokenized Golden Standard file will
		# be stored in a list (similar to the trainingCorpus)
		self._goldenCorpus = []

		# The Golden Standard Tag Set will be stored as a set
		self._goldenTagSet = set()

		# We need to remember the total number of errors
		self._totalErrors = 0

		# As well as the errors due to unknown words
		self._totalUnknownErrors = 0

		self.LearnGoldenStandard(goldenFileName)

	def LearnGoldenStandard(self, goldenFileName):
		try:
			# Tokenize the Golden Standard text file by splitting
			# on whitespace first, then for each element in
			# the list, we split on '/'.
			# This results in a list of lists, of the form
			# [[word1, tag1], [word2, tag2], ...]
			with open(goldenFileName) as goldenFile:
				self._goldenCorpus = list(x.split('/') for x in goldenFile.read().split())
		except IOError:
			print(f'Error: Could not open {goldenFileName}')
			print('Call \'LearnTestSet(FileName)\' to read the correct file.')
		else:
			# Extract the tagset from this corpus and the tags we would have predicted for it
			for wordTagPair in self._goldenCorpus:
				self._goldenTagSet.add(wordTagPair[1])
				self._goldenTagSet.add(self._mostLikelyTags.get(wordTagPair[0], "NN"))

			# Remember to add NN for unknown words
			self._goldenTagSet.add("NN")

			# Initialise the confusion matrix to zero
			self._initializeConfusionMatrix()

			# Now compute the Confusion Matrix
			self._computeConfusionMatrix()


	def DisplayConfusionMatrix(self):
		print("The Confusion Matrix might be too large for console output.")
		print("So it will be displayed in your default text editor instead.")
		print("Be sure to disable Word Wrapping to allow horizontal scrolling.")
		print("In Notepad, untick: Format >> Word Wrap")

		with open("confusion_matrix.txt", "w") as f:
			print("-----------------", file=f)
			print("Confusion Matrix:", file=f)
			print("-----------------", file=f)

			# Print the header
			header = f"{'':^8s}"
			for tag in self._confusionMatrix:
				header += f"{tag:^8s}"
			print(header, file=f)

			for outerTag in self._confusionMatrix:
				line = f"{outerTag:^8s}"
				innerDict = self._confusionMatrix[outerTag]
				for innerTag in innerDict:
					innerValue = round(innerDict[innerTag], 5)
					line += f"{str(innerValue) if innerValue != 0 else '-':^8s}"
				
				print(line, file=f)

			print("-------------------------------------------------------", file=f)
			print(f"Total Errors: {self._totalErrors} ({self._totalUnknownErrors} of which are due to unknown words)", file=f)
			print(f"Accuracy: {round(((len(self._goldenCorpus) - self._totalErrors) / len(self._goldenCorpus) * 100), 5)}%", file=f)
			print("-------------------------------------------------------\n", file=f)

		# The Confusion Matrix might be too large for console output,
		# so we open it in the default text editor instead
		webbrowser.open("confusion_matrix.txt")

	def _initializeConfusionMatrix(self):
		# Initialise the confusion matrix to zero
		for outerTag in self._goldenTagSet:
			innerDict = dict()
			for innerTag in self._goldenTagSet:
				innerDict[innerTag] = 0
			
			self._confusionMatrix[outerTag] = innerDict

	def _computeConfusionMatrix(self):
		self._totalErrors = 0
		self._totalUnknownErrors = 0
		for wordTagPair in self._goldenCorpus:
			word = wordTagPair[0]
			correctTag = wordTagPair[1]
			predictedTag = self._mostLikelyTags.get(word, "NN")

			if correctTag != predictedTag:
				# Increment the number of errors so far
				self._totalErrors += 1

				# Increment the error count for these tags
				self._confusionMatrix[correctTag][predictedTag] += 1

				if predictedTag == "NN":
					self._totalUnknownErrors += 1

		# Finally, convert each count in the Confusion Matrix to a percentage
		# provided that there was at least one error
		if self._totalErrors != 0:
			for outerTag in self._confusionMatrix:
				for innerTag in self._confusionMatrix[outerTag]:
					self._confusionMatrix[outerTag][innerTag] /= self._totalErrors



def main():
	print("--------------------------------------------------------------------------------------------------")
	print("This program accepts a 'golden standard' file and prints a Confusion Matrix for the trained corpus")
	print("--------------------------------------------------------------------------------------------------\n")
	
	# Instantiate our error analyzer
	mla = MostLikelyTagAnalyzer()

	# Display the computed confusion matrix
	mla.DisplayConfusionMatrix()

	# Wait for input to continue
	input("\nPress <RETURN> to continue")

if __name__ == "__main__":
	print("\n===============================================")
	print("62760858 - COS4861 - Assignment 2 - 2021 - Q3_3")
	print("===============================================\n")
	main()