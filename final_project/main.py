import engine

def main():
    while True:
        print("\n==============================")
        print("      THE DIGITAL SOUS-CHEF   ")
        print("==============================")
        print("1. View Pantry")
        print("2. Add Loot (Ingredients)")
        print("3. Find Recipes")
        print("4. Start Cooking")
        print("5. View Cooking History") # New Option!
        print("6. Exit")
        
        choice = input("\nAction: ")

        if choice == '1': engine.view_pantry()
        elif choice == '2': engine.add_loot()
        elif choice == '3': engine.find_recipes()
        elif choice == '4': engine.cook_recipe()
        elif choice == '5': engine.view_history() # Call the new function
        elif choice == '6': 
            print("Game Saved. Goodbye!")
            break
        else: 
            print("Invalid choice.")

if __name__ == "__main__":
    main()