"""
Student Information and Grade Calculator.

This program takes a student's personal details and quiz scores via user input.
It processes the data to format the full name, calculates the average of the 
two quizzes, and displays a summary of the results.
"""

# Take user input.
lastName = input("Enter your last name: ")
firstName = input("Enter your first name: ")
middleName = input("Enter your middle name: ")
course = input("Enter your course: ")
quiz1 = int(input("Enter your quiz 1 score: "))
quiz2 = int(input("Enter your quiz 2 score: "))

#Combine the names into a full name.
fullName = lastName + ", " + firstName + " " + middleName

#Calculate the average quiz score.
averageQuizScore = float((quiz1 + quiz2) / 2)

#Display the results.
print("\n--- Student Information ---")
print("Full Name: " + fullName)
print("Course: " + course)
print(f"Average Quiz Score:  {averageQuizScore:.2f}")