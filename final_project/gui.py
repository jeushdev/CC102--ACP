import customtkinter as ctk
import engine

class SousChefApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("The Digital Sous-Chef")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")

        # 1. Create Grid Layout (1 column for sidebar, 1 for content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="KITCHEN QUEST", font=("Roboto", 20, "bold"))
        self.logo.pack(pady=20)

        # 3. Sidebar Buttons
        self.btn_pantry = ctk.CTkButton(self.sidebar, text="My Pantry", command=self.show_pantry)
        self.btn_pantry.pack(pady=10, padx=20)

        self.btn_recipes = ctk.CTkButton(self.sidebar, text="Find Recipes", command=self.show_recipes)
        self.btn_recipes.pack(pady=10, padx=20)

        # 4. Main Content Area
        self.main_view = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.main_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def show_pantry(self):
        # Clear the frame
        for widget in self.main_view.winfo_children():
            widget.destroy()
            
        # Add labels for each item in the pantry
        pantry_data = engine.data_manager.load_data(engine.data_manager.PANTRY_FILE)
        ctk.CTkLabel(self.main_view, text="Current Inventory", font=("Arial", 24)).pack(pady=10)
        
        for item, info in pantry_data.items():
            label = ctk.CTkLabel(self.main_view, text=f"{item.capitalize()}: {info['amount']} {info['unit']}")
            label.pack(anchor="w", padx=20)

    def show_recipes(self):
        # This is where we will render the "Recipe Cards"
        pass

if __name__ == "__main__":
    app = SousChefApp()
    app.mainloop()