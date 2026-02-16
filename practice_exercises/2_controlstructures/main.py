"""
IT Support Ticket System

Purpose:
This program automates the classification of IT support tickets. It determines 
the priority level (P1-P4) and Service Level Agreement (SLA) target time based 
on the user-defined impact and urgency. It also generates specific troubleshooting 
steps based on the issue category.

Expected Inputs:
- Employee Name (string)
- Department (string)
- Issue Category (string): 'network', 'hardware', or 'software'
- Impact Level (int): 1 (Low), 2 (Medium), 3 (High)
- Urgency Level (int): 1 (Low), 2 (Medium), 3 (High)

Expected Outputs:
- A formatted ticket summary displaying:
  - Calculated Priority (Critical, High, Medium, Low)
  - SLA Target (4, 8, 24, or 72 hours)
  - Category-specific troubleshooting note
"""

# Take user input for IT support ticket
name = input("Enter employee name: ")
department = input("Enter department: ")
category = input("Enter issue category (network/hardware/software): ").lower()
impact_lvl = int(input("Enter impact level (1-3): "))
urgency_lvl = int(input("Enter urgency level (1-3): "))

# Determine priority based on impact and urgency levels
priority = ""
if impact_lvl == 3 and urgency_lvl == 3:
    priority = "P1 (Critical)"
elif impact_lvl >= 2 and urgency_lvl >= 2:
    priority = "P2 (High)"
elif impact_lvl >= 2 and urgency_lvl == 1:
    priority = "P3 (Medium)"
else:
    priority = "P4 (Low)"
    
# Determine SLA Target based on Priority
sla_target = 0
if "P1" in priority:
    sla_target = 4
elif "P2" in priority:
    sla_target = 8
elif "P3" in priority:
    sla_target = 24
else:
    sla_target = 72


# Print the output ticket summary
print("")
print(f"Employee: {name}")
print(f"Department: {department}")
print(f"Category: {category.capitalize()}")
print(f"Impact: {impact_lvl}")
print(f"Urgency: {urgency_lvl}")
print(f"Priority: {priority}")
print(f"SLA Target: {sla_target} hours")
print("Note: ",  end="")

# Determine troubleshooting steps based on issue category
if category == "network":
    print("Check connectivity and ISP status.")
elif category == "hardware":
    print("Check device condition and peripherals.")
else:
    # Captures 'software' and any other input
    print("Check application errors and updates.")