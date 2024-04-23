#Mason Thomas
#CapstoneProject
#GUI Dev


import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox

class TravelPlannerApp:
    def __init__(self, master):
        
        self.master = master
        self.master.title("Travel Planner")

        # Read seasons and activities from file
        self.seasons_activities = self.read_seasons_activities("season.txt")

        # Create frames for different sections
        self.location_frame = tk.Frame(master)
        self.location_frame.pack()

        self.activity_frame = tk.Frame(master)
        self.activity_frame.pack()

        self.payment_frame = tk.Frame(master)
        self.payment_frame.pack()

        # Initialize variables
        self.selected_season = tk.StringVar()
        self.selected_activity = tk.StringVar()
        self.selected_add_item = tk.StringVar()
        self.selected_items = []

        # Location Recommendation Section
        self.season_label = tk.Label(self.location_frame, text="Select season:")
        self.season_label.grid(row=0, column=0)

        self.seasons = list(self.seasons_activities.keys())
        self.season_combobox = ttk.Combobox(self.location_frame, textvariable=self.selected_season, values=self.seasons)
        self.season_combobox.grid(row=0, column=1)

        self.activity_label = tk.Label(self.location_frame, text="Select activity:")
        self.activity_label.grid(row=1, column=0)

        self.activity_combobox = ttk.Combobox(self.location_frame, textvariable=self.selected_activity)
        self.activity_combobox.grid(row=1, column=1)

        self.find_locations_button = tk.Button(self.location_frame, text="Find Locations", command=self.find_locations)
        self.find_locations_button.grid(row=2, columnspan=2)

        self.location_results = tk.Frame(self.location_frame, width=400, height=200)
        self.location_results.grid(row=3, columnspan=2)
        self.location_results.configure(borderwidth="2")
        self.location_results.configure(relief="groove")

        

        # Add Item Section
        self.add_item_label = tk.Label(self.activity_frame, text="Dont want to pack? Well do it for you!\nSelect yes to add a care package for your excursion!")
        self.add_item_label.grid(row=1, column=0)

        self.add_item_yes = tk.Radiobutton(self.activity_frame, text="Yes", variable=self.selected_add_item, value="Yes")
        self.add_item_yes.grid(row=2, column=0)

        self.add_item_no = tk.Radiobutton(self.activity_frame, text="No", variable=self.selected_add_item, value="No")
        self.add_item_no.grid(row=3, column=0)

        # Payment Portal Section
        self.payment_label = tk.Label(self.payment_frame, text="Payment Summary:")
        self.payment_label.grid(row=0, column=0)

        self.payment_text = tk.Text(self.payment_frame, width=50, height=10)
        self.payment_text.grid(row=1, column=0)

        self.calculate_total_button = tk.Button(self.payment_frame, text="Calculate Total", command=self.calculate_total)
        self.calculate_total_button.grid(row=2, column=0)

        # Update activity combobox options based on selected season
        self.selected_season.trace("w", self.update_activity_options)

    def read_seasons_activities(self, filename):
        seasons_activities = {}
        with open(filename, "r") as file:
            season = ""
            for line in file:
                line = line.strip()
                if line:
                    if line.startswith("#"):
                        season = line[1:].strip()
                        seasons_activities[season] = []
                    else:
                        # Split the line into activity and price
                        parts = line.split(":")
                        if len(parts) == 2:  # Check if both activity and price are present
                            activity, price = parts
                            seasons_activities[season].append((activity.strip(), float(price.strip())))
                        else:
                            print(f"Ignoring invalid line: {line}")
        return seasons_activities

    def update_activity_options(self, *args):
        selected_season = self.selected_season.get()
        if selected_season:
            activities_with_prices = self.seasons_activities[selected_season]
            activities = [activity for activity, _ in activities_with_prices]  # Extract activities
            self.activity_combobox.config(values=activities)

    def find_locations(self):
        selected_activity = self.selected_activity.get()
        selected_season = self.selected_season.get()

        # Retrieve price for selected activity
        activities_with_prices = self.seasons_activities[selected_season]
        for activity, price in activities_with_prices:
            if activity == selected_activity:
                self.location_price = price
                break

        # Display location price
        self.payment_text.insert(tk.END, f"{selected_activity} Trip: ${self.location_price}\n")


        # Display image based on season and activity
        imageFile = f"{selected_season.lower()}_{selected_activity.lower().replace(' ', '_')}.png"
        try:
            frame = self.location_results
            img = Image.open(imageFile)
            photo = ImageTk.PhotoImage(img.resize((400, 200)))
            lblImage = ttk.Label(frame, image=photo)
            lblImage.image = photo
            lblImage.place(relx=.5, rely=.5, anchor=CENTER)

        except FileNotFoundError:
            print("Image not found.")

        self.add_care_package()

    def add_care_package(self):
        answer = self.selected_add_item.get()
        if answer == "Yes":
            self.package_price = 49.99
            self.payment_text.insert(tk.END, f"Package Price: ${self.package_price}\n")
        else:
            self.package_price = 0
    
    def calculate_total(self):
        self.total_cost = 0

        self.add_care_package()

        self.total_cost += self.location_price
        self.total_cost += self.package_price

        # Display receipt with selected items and total cost in self.payment_text
        payment_summary = self.payment_text.get("1.0", tk.END)

        # Add total cost to the payment summary
        payment_summary += f"\nTotal Cost: ${self.total_cost:.2f}\n"
        payment_summary += "OK to pay(closes the program)"

        # Show the payment summary with total cost in a messagebox
        messagebox.showinfo("Payment Summary", payment_summary)

        # Close the program
        self.master.destroy()

        


def main():
    root = tk.Tk()
    app = TravelPlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

