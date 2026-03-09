"""
Weekly Payroll Slip System
Processes and records weekly payroll slips for employees including their
weekly and gross pay, government deductions, and net pay. 
"""

while True:
    # Take user details
    employee_name = input("Enterr Employee Name: ")

    if employee_name == "END":
        break

    hours_worked = float(input("Enter Hours Worked: "))
    hourly_rate = float(input("Enter Hourly Rate: "))
    night_hours = float(input("Enter Night Hours: "))


    # Calculate employees weekly pay including regular, overtime, night hours
    if hours_worked <= 40:
        regular_pay = hours_worked * hourly_rate
        overtime_pay = 0
    else:
        regular_pay = 40 * hourly_rate
        overtime_pay = (hours_worked - 40) * (hourly_rate * 1.25)
    
    night_pay = night_hours * (hourly_rate * 0.10)

    gross_pay = regular_pay + overtime_pay + night_pay

    # Calculate and deduct government deductions and tax
    sss = gross_pay * .045
    philhealth = gross_pay * 0.02
    pagibig = gross_pay * 0.02
    
    gov_deductions = sss + philhealth + pagibig

    if gross_pay <= 5000:
        tax = 0
    elif 5000 < gross_pay <= 10000:
        tax = gross_pay * .1
    else:
        tax = gross_pay * .15
    
    net_pay = gross_pay - gov_deductions - tax

    # Print employee's payroll slip
    print()
    print("WEEKLY PAYROLL CALCULATOR")
    print("=" * 60)
    print(f"{'Employee Name':30} : {employee_name}")
    print(f"{'Hours Worked':30} : {hours_worked:,.2f}")
    print(f"{'Hourly Rate':30} : {hourly_rate:,.2f}")
    print(f"{'Night Hours':30} : {night_hours:,.2f}")
    print("=" * 60)
    print(f"{'Regular Pay':30} : {regular_pay:,.2f}")
    print(f"{'Overtime Pay':30} : {overtime_pay:,.2f}")
    print(f"{'Night Differential':30} : {night_pay:,.2f}")
    print("-" * 60)
    print(f"{'Gross Pay':30} : {gross_pay:,.2f}")
    print("-" * 60)
    print(f"{'SSS (4.5%)':30} : {sss:,.2f}")
    print(f"{'PhilHealth (2%)':30} : {philhealth:,.2f}")
    print(f"{'Pag-IBIG (2%)':30} : {pagibig:,.2f}")
    print(f"{'Withholding Tax':30} : {tax:,.2f}")
    print("-" * 60)
    print(f"{'NET PAY':30} : {net_pay:,.2f}")

