import data_manager
from datetime import datetime

# Items we don't want to "track" or require the user to "buy"
INFINITE_ITEMS = ["salt", "water", "pepper", "oil", "sugar"]

def view_pantry():
    pantry = data_manager.load_data(data_manager.PANTRY_FILE)
    if not pantry:
        print("\n[!] Your pantry is empty. Time to go looting!")
    else:
        print("\n--- CURRENT INVENTORY ---")
        for item, info in pantry.items():
            print(f"- {item.capitalize()}: {info['amount']} {info['unit']}")

def add_loot():
    pantry = data_manager.load_data(data_manager.PANTRY_FILE)
    print("\n--- LOOTING MODE ---")
    print("Type 'exit' as the item name to return to menu.")

    while True:
        name = input("\nEnter item name: ").lower().strip()
        if name == "exit":
            break
            
        try:
            amt_input = input(f"How much {name} did you find? ")
            if amt_input.lower() == "exit": break
            amt = float(amt_input)
        except ValueError:
            print("[!] Error: Please enter a number.")
            continue

        unit = input(f"Unit for {name} (pc/g/ml): ")
        if unit.lower() == "exit": break

        if name in pantry:
            pantry[name]['amount'] += amt
        else:
            pantry[name] = {"amount": amt, "unit": unit}
        
        data_manager.save_data(data_manager.PANTRY_FILE, pantry)
        print(f"[+] Updated: {name} increased by {amt}.")

def get_missing(recipe_ingredients, pantry):
    """Calculates the delta between required and owned ingredients."""
    missing = {}
    for item, req in recipe_ingredients.items():
        if item.lower() in INFINITE_ITEMS:
            continue
            
        owned = pantry.get(item, {}).get("amount", 0)
        if owned < req['amount']:
            missing[item] = {"amount": req['amount'] - owned, "unit": req['unit']}
    return missing

def find_recipes():
    pantry = data_manager.load_data(data_manager.PANTRY_FILE)
    cookbook = data_manager.load_data(data_manager.RECIPES_FILE)
    
    print("\n⭐ AVAILABLE QUESTS (100% Match) ⭐")
    for r_id, r_data in cookbook.items():
        if not get_missing(r_data['ingredients'], pantry):
            print(f" > {r_data['name']} (ID: {r_id})")

    print("\n🔒 LOCKED QUESTS (1-3 items missing) 🔒")
    for r_id, r_data in cookbook.items():
        miss = get_missing(r_data['ingredients'], pantry)
        if 0 < len(miss) <= 3:
            miss_str = ", ".join([f"{v['amount']}{v['unit']} {k}" for k, v in miss.items()])
            print(f" x {r_data['name']} (Need: {miss_str})")

def cook_recipe():
    pantry = data_manager.load_data(data_manager.PANTRY_FILE)
    cookbook = data_manager.load_data(data_manager.RECIPES_FILE)

    recipe_id = input("\nEnter Recipe ID to cook: ").lower()
    if recipe_id not in cookbook:
        return print("[!] Recipe ID not found.")

    recipe = cookbook[recipe_id]
    missing = get_missing(recipe['ingredients'], pantry)

    if missing:
        return print("[!] You don't have enough loot to craft this!")

    print(f"\n--- COOKING: {recipe['name']} ---")
    for i, step in enumerate(recipe['steps'], 1):
        print(f"{i}. {step}")

    # Subtract ingredients
    for item, req in recipe['ingredients'].items():
        if item.lower() not in INFINITE_ITEMS:
            pantry[item]['amount'] -= req['amount']
            if pantry[item]['amount'] <= 0:
                del pantry[item]
    
    data_manager.save_data(data_manager.PANTRY_FILE, pantry)
    log_cooking(recipe['name'])
    print("\n[✔] Quest Complete! History updated.")

def log_cooking(recipe_name):
    history = data_manager.load_data(data_manager.HISTORY_FILE)
    if isinstance(history, dict): history = [] 

    new_entry = {
        "recipe_name": recipe_name,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history.append(new_entry)
    data_manager.save_data(data_manager.HISTORY_FILE, history)

def view_history():
    history = data_manager.load_data(data_manager.HISTORY_FILE)
    if not history:
        return print("\n[!] No history found.")

    print("\n--- COOKING HISTORY LOG ---")
    counts = {}
    for entry in history:
        print(f"[{entry['date']}] {entry['recipe_name']}")
        counts[entry['recipe_name']] = counts.get(entry['recipe_name'], 0) + 1

    print("\n--- 🏆 CULINARY ACHIEVEMENTS 🏆 ---")
    for name, total in counts.items():
        rank = "Novice"
        if total >= 10: rank = "Master"
        elif total >= 5: rank = "Expert"
        print(f"- {name}: Cooked {total}x ({rank})")