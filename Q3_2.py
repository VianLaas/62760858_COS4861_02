import webbrowser
from Q3_1 import MostLikelyTagEstimator
import re

class MostLikelyTagAnnotator(MostLikelyTagEstimator):
	def __init__(self, trainingFileName = 'pos_tagged.txt', testFileName = 'pos_test.txt'):
		super().__init__(trainingFileName)

		# The Test Set will be stored as a list
		self._testSet = []

		# The annotated words from the test
		# set will be stored as a list
		self._annotatedWords = []

		# Read the test file to build the Test Set
		self.AnnotateTestSet(testFileName)

	def AnnotateTestSet(self, testFileName):
		try:
			# Tokenize the test text file by inserting spaces 
			# between words and puncuation (using regex) and
			# then splitting the resulting string on spaces.
			# This results in a list of words from the Test Set
			with open(testFileName) as testFile:
				testString = testFile.read()
		except IOError:
			print(f'Error: Could not open {testFileName}')
			print('Call \'LearnTestSet(FileName)\' to read the correct file.')
		else:
			# Insert spaces between words and punctuation marks
			testString = re.sub(r'(\w+)([.,\'"`!?])', r'\1 \2', testString)

			# Insert spaces between punctuation marks and words
			testString = re.sub(r'([.,\'"`!?])(\w+)', r'\1 \2', testString)

			# Insert spaces between words and formatting characters (\n \t and \r)
			testString = re.sub(r'([\t\n\r])([\w.,\'"!?])', r'\1 \2', testString)

			# Insert spaces between formatting characters and words
			testString = re.sub(r'([\w.,\'"!?])([\t\n\r])', r'\1 \2', testString)

			# Split this formatted string into the Test Set
			self._testSet = testString.split(" ")

			# Now annotate the Test Set with the most likely tags for each word
			for word in self._testSet:
				if not re.search(r'[\t\n\r]', word[0]):
					self._annotatedWords.append(word + "/" + self._mostLikelyTags.get(word, "NN"))
				else:
					# Don't annotate format characters
					self._annotatedWords.append(word)

			# Save the annotated words as a new file in a human-readable format
			newFileName = f"annotated_{testFileName}"
			with open(newFileName, "w") as annotatedFile:
				annotatedFile.write(self.AnnotatedFileContents())

			print(f"File '{newFileName}' created")

			webbrowser.open(newFileName)

	def AnnotatedFileContents(self):
		return str.join(" ", self._annotatedWords)

def main():
	print("------------------------------------------------------------------------------------------------------------------------------------")
	print("This program accepts a file as an input parameter and produces an annotated file containing POS tags for each word in the input file")
	print("------------------------------------------------------------------------------------------------------------------------------------\n")

	# Instantiate our annotator
	mla = MostLikelyTagAnnotator()

	# Display the generated file's contents
	print("---------------------------")
	print("Contents of annotated file:")
	print("---------------------------\n")
	print(mla.AnnotatedFileContents())

	# Wait for input to continue
	input("\nPress <RETURN> to continue")

if __name__ == "__main__":
	print("\n===============================================")
	print("62760858 - COS4861 - Assignment 2 - 2021 - Q3_2")
	print("===============================================\n")
	main()