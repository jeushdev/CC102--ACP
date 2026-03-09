"""
Monthly Electric Billing System
Calculates and print monthly electricity billing statements including 
tiered consumption charges, VAT, and lifeline discounts.
"""

while True: 
    # Take user details
    customer_name = input("Enter Customer Name: ")

    # Sentinel
    if customer_name == "END":
        break

    kilowatt_hours_used = float(input("Enter kWh Used: "))

    # Calculate the charges by rate
    if kilowatt_hours_used <= 100:
        energy_charge = kilowatt_hours_used * 10.00
    elif kilowatt_hours_used <= 200:
        energy_charge = (100 * 10) + (kilowatt_hours_used - 100) * 12.00
    else:
        energy_charge = ((kilowatt_hours_used - 200) * 15) + 2200
    
    generation_charge = kilowatt_hours_used * 3.50
    distribution_charge = kilowatt_hours_used * 2.00
    system_loss_charge = kilowatt_hours_used * 1.50

    subtotal_charge = energy_charge + generation_charge + distribution_charge + system_loss_charge

    # Calculate and deduct applicable discounts
    if kilowatt_hours_used <= 100:
        discount = subtotal_charge * 0.10
    else:
        discount = 0.00

    vat = subtotal_charge * 0.12
    

    total_charge = subtotal_charge + vat - discount

    # Print the Billing details
    print("\n\nELECTRICITY BILL")
    print("=" * 60)
    print(f"{'Customer Name':20} : {customer_name}")
    print(f"{'Energy Consumption':20} : {kilowatt_hours_used:,.2f} kWh")
    print("=" * 60)
    print(f"{'Energy Charge':20} : {energy_charge:,.2f}")
    print(f"{'Generation Charge':20} : {generation_charge:,.2f}")
    print(f"{'Distribution Charge':20} : {distribution_charge:,.2f}")
    print(f"{'System Loss Charge':20} : {system_loss_charge:,.2f}")
    print("-" * 60)
    print(f"{'Subtotal':20} : {subtotal_charge:,.2f}")
    print(f"{'VAT (12%)':20} : {vat:,.2f}")
    print(f"{'Lifeline Discount':20} : {discount:,.2f}")
    print("-" * 60)
    print(f"{'TOTAL AMOUNT DUE':20} : {total_charge:,.2f}")
    print("=" * 60)
    print()
