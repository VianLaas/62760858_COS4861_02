import Q3_1
import Q3_2
import Q3_3

options = ["Question 3.1 (Q3_1)", "Question 3.2 (Q3_2)", "Question 3.3 (Q3_3)", "Exit"]

while True:
	print("\n========================================")
	print("62760858 - COS4861 - Assignment 2 - 2021")
	print("========================================\n")
	print("Please enter the question you wish to run: (e.g. Q3_1)")
	for option in options:
		print(">> " + option)
	questionNumber = input(":: ").upper()
	print()

	if questionNumber == "EXIT":
		break
	elif questionNumber == "Q3_1":
		Q3_1.main()
	elif questionNumber == "Q3_2":
		Q3_2.main()
	elif questionNumber == "Q3_3":
		Q3_3.main()
	else:
		print("Error: Invalid input")