import tkinter as tk
from tkinter import messagebox
import threading
from advanced_amazon_price_tracker import run_price_checker, products

class AmazonPriceTrackerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Amazon Price Tracker")

        self.label = tk.Label(master, text="Amazon Price Tracker")
        self.label.pack()

        self.check_prices_button = tk.Button(master, text="Check Prices Now", command=self.check_prices)
        self.check_prices_button.pack()

        self.product_listbox = tk.Listbox(master, width=50)
        self.product_listbox.pack()

        for _, name, threshold in products:
            self.product_listbox.insert(tk.END, f"{name} (Threshold: ₹{threshold})")

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

    def check_prices(self):
        self.check_prices_button.config(state=tk.DISABLED)
        threading.Thread(target=self.run_price_check, daemon=True).start()

    def run_price_check(self):
        run_price_checker()
        self.master.after(0, self.enable_check_button)

    def enable_check_button(self):
        self.check_prices_button.config(state=tk.NORMAL)
        messagebox.showinfo("Price Check Complete", "Prices have been checked and updated.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = AmazonPriceTrackerGUI(root)
    root.mainloop()