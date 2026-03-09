"""
!AI GENERATED (tinamad naku)
Student Tuition and Assessment Billing System
Generates a formatted Registration Form for Batangas State University
             graduate students. It calculates tuition, fixed assessment fees, 
             and the General Development Fee based on enrolled units.
"""

# Fixed Assessment Fees and Rates
TUITION_RATE = 500.00
GDF_RATE = 86.00
LIBRARY_FEE = 751.00
REGISTRATION_FEE = 380.00
MEDICAL_DENTAL_FEE = 547.20
JOURNAL_FEE = 751.00

# 1. Use a while loop to repeatedly process student records
while True:
    print("-" * 70)
    student_name = input("Enter Student Name (or 'END' to quit): ")
    
    # 2. Use a break statement with the sentinel value "END"
    if student_name.upper() == "END":
        break
        
    sr_code = input("Enter SR Code: ")
    sex = input("Enter Sex: ")
    program = input("Enter Program: ")
    section = input("Enter Section: ")
    
    # Course Information
    num_courses = int(input("Enter Number of Courses: "))
    
    # Variables to store course data and accumulate total units
    courses_list = []
    total_units = 0 # 4. Use variables to accumulate total units
    
    # 3. Use a nested loop (for loop) to process multiple courses
    for i in range(num_courses):
        print(f"\nCourse {i + 1}")
        course_code = input("Enter Course Code: ")
        course_title = input("Enter Course Title: ")
        units = int(input("Enter Units: "))
        
        # Store course details in a list to print in the table later
        courses_list.append([course_code, course_title, units])
        total_units += units # Accumulation
        
    # 5. Use appropriate arithmetic operations for computations
    tuition_total = total_units * TUITION_RATE
    gdf_total = total_units * GDF_RATE
    
    total_payable = (tuition_total + LIBRARY_FEE + REGISTRATION_FEE + 
                     MEDICAL_DENTAL_FEE + JOURNAL_FEE + gdf_total)
    
    # 6 & 7. Use formatted output (f-strings) and 2 decimal places
    print("\nSECOND SEMESTER, 2023-2024")
    print("REGISTRATION FORM")
    print("=" * 70)
    print(f"{'SR Code':15} : {sr_code}")
    print(f"{'Name':15} : {student_name.upper()}")
    print(f"{'Sex':15} : {sex.upper()}")
    print(f"{'Program':15} : {program}")
    print(f"{'Section':15} : {section.upper()}")
    print("=" * 70)
    
    # COURSE DETAILS TABLE
    print("COURSE DETAILS")
    print(f"{'CODE':12} {'COURSE TITLE':40} {'UNITS'}")
    for course in courses_list:
        print(f"{course[0]:12} {course[1]:40} {course[2]}")
        
    print("-" * 70)
    print(f"Total Units {total_units:>54}")
    print("=" * 70)
    
    # ASSESSMENT SECTION
    print("ASSESSMENT")
    print(f"{'Tuition Fee (' + str(TUITION_RATE) + '0/unit)':40} : {tuition_total:10,.2f}")
    print(f"{'Library Fee':40} : {LIBRARY_FEE:10,.2f}")
    print(f"{'Registration Fee':40} : {REGISTRATION_FEE:10,.2f}")
    print(f"{'Medical / Dental Fee':40} : {MEDICAL_DENTAL_FEE:10,.2f}")
    print(f"{'GDF (' + str(GDF_RATE) + '0/unit)':40} : {gdf_total:10,.2f}")
    print(f"{'Journal Fee':40} : {JOURNAL_FEE:10,.2f}")
    print("-" * 70)
    print(f"{'TOTAL (PHP)':40} : {total_payable:10,.2f}")
    print("=" * 70 + "\n")