

import customtkinter as ctk
from tkinter import filedialog, simpledialog, messagebox, StringVar, Listbox
from PIL import Image, ImageTk, ImageDraw
import json
import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))

def install_r():
    os.system(f"pip install -r {script_dir}\\requirements.txt")
    os.system("pip install customtkinter && pip install pillow")
install_r()




class SilentMessageBox:
    @staticmethod
    def showinfo(title, message):
        top = ctk.CTkToplevel()
        top.title(title)
        ctk.CTkLabel(top, text=message).pack(padx=20, pady=20)
        ctk.CTkButton(top, text="Ok", command=top.destroy).pack()
        top.transient(root)
        top.grab_set()
        root.wait_window(top)

class MapGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Click Game")
        # global place_name_
        self.image_label = None
        self.map_image = None
        self.map_draw = None
        self.map_path = None
        self.coordinates = []
        self.presets = {}
        self.current_preset = None
        self.current_round = 0
        self.guess_event = StringVar()
        self.guess_x, self.guess_y = 0, 0  
        self.load_presets()

        self.title_label = ctk.CTkLabel(root, text="Map GAME", font=("fixedsys", 24))
        self.title_label.pack(pady=10)
        
        

        self.load_button = ctk.CTkButton(root, text="Load Map", command=self.load_map)
        self.load_button.pack(pady=10)

        self.play_button = ctk.CTkButton(root, text="Play", command=self.play_game)
        self.play_button.pack(pady=10)

        self.reset_button = ctk.CTkButton(root, text="Reset", command=self.reset_presets)
        self.reset_button.pack(pady=10)

        self.upload_button = ctk.CTkButton(root, text="Upload Preset", command=self.upload_preset)
        self.upload_button.pack(pady=10)

        self.dark_mode_switch = ctk.CTkSwitch(self.root, text="Light Mode", command=self.toggle_dark_mode)
        self.dark_mode_switch.pack(pady=10)


        self.quit = ctk.CTkButton(root, text="Quit", command=lambda: self.root.destroy())
        self.quit.pack(pady=10)
    def load_map(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.map_path = file_path
            self.map_image = Image.open(self.map_path)
            self.map_image = self.map_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
            self.map_draw = ImageDraw.Draw(self.map_image)
            self.map_image_tk = ImageTk.PhotoImage(self.map_image)

            if self.image_label:
                self.image_label.destroy()

            self.image_label = ctk.CTkLabel(self.root, image=self.map_image_tk)
            self.image_label.pack(fill="both", expand=True)
            self.image_label.bind("<Button-1>", self.record_coordinates)

            self.hide_main_buttons()

            self.close_button = ctk.CTkButton(self.root, text="Close", command=self.close_map)
            self.close_button.place(relx=0.9, rely=0.05, anchor="ne")

    def close_map(self):
        if self.current_preset:
            self.return_to_main_screen()
        else:
            save_option = messagebox.askyesno("Save Map", "Would you like to save the recorded places?")
            if save_option:
                preset_name = simpledialog.askstring("Preset Name", "Enter a name for this preset:")
                if preset_name:
                    self.presets[preset_name] = {
                        "coordinates": self.coordinates.copy(),
                        "map_path": self.map_path
                    }
                    self.save_presets()
                    messagebox.showinfo("Success", f"Preset '{preset_name}' saved successfully!")
            self.return_to_main_screen()

    def return_to_main_screen(self):
        if self.image_label:
            self.image_label.destroy()
        if self.close_button:
            self.close_button.destroy()
        self.show_main_buttons()

    def hide_main_buttons(self):
        self.load_button.pack_forget()
        self.play_button.pack_forget()
        self.reset_button.pack_forget()
        self.upload_button.pack_forget()
        self.title_label.pack_forget()
        self.quit.pack_forget()
        self.dark_mode_switch.pack_forget()
    def show_main_buttons(self):
        self.title_label.pack(pady=10)
        self.load_button.pack(pady=10)
        self.play_button.pack(pady=10)
        self.reset_button.pack(pady=10)
        self.upload_button.pack(pady=10)
        self.quit.pack(pady=10)
        self.dark_mode_switch.pack()
    def record_coordinates(self, event):
        x, y = event.x, event.y
        place_name_ = simpledialog.askstring("Place Name", "Enter the name of the place:")

        if place_name_:
            self.coordinates.append({"x": x, "y": y, "name": place_name_})
            self.draw_dot_with_label(x, y, place_name_)

    def draw_dot_with_label(self, x, y, name):
        radius = 5
        self.map_draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="red", outline="red")
        self.map_draw.text((x + 8, y - 8), name, fill="red")
        self.map_image_tk = ImageTk.PhotoImage(self.map_image)
        self.image_label.configure(image=self.map_image_tk)

    def play_game(self):
        if not self.presets:
            messagebox.showwarning("No Presets", "No presets available to play. Load a map and create a preset first.")
            return

        preset_name = self.select_preset_from_list()
        if preset_name:
            self.hide_main_buttons()
            self.current_preset = preset_name
            preset_data = self.presets[preset_name]
            self.coordinates = preset_data["coordinates"]
            self.map_path = preset_data["map_path"]
            self.load_map_for_play()
            self.current_round = 0
            self.start_round()

    def select_preset_from_list(self):
        preset_window = ctk.CTkToplevel(self.root)
        preset_window.title("Select Preset")

        preset_listbox = Listbox(preset_window, height=10)
        preset_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        for preset_name in self.presets:
            preset_listbox.insert("end", preset_name)
        preset_listbox.lift()
        def select_and_close():
            try:
                selected = preset_listbox.get(preset_listbox.curselection())
                preset_window.destroy()
                self.guess_event.set(selected)
            except IndexError:
                messagebox.showwarning("Selection Error", "Please select a preset.")

        select_button = ctk.CTkButton(preset_window, text="Select", command=select_and_close)
        select_button.pack(pady=5)
        self.root.wait_variable(self.guess_event)
        return self.guess_event.get()

    def load_map_for_play(self):
        self.map_image = Image.open(self.map_path)
        self.map_image = self.map_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.LANCZOS)
        self.map_draw = ImageDraw.Draw(self.map_image)
        self.map_image_tk = ImageTk.PhotoImage(self.map_image)

        if self.image_label:
            self.image_label.destroy()

        self.image_label = ctk.CTkLabel(self.root, image=self.map_image_tk)
        self.image_label.pack(fill="both", expand=True)

        self.close_button = ctk.CTkButton(self.root, text="Close", command=self.return_to_main_screen)
        self.close_button.place(relx=0.9, rely=0.05, anchor="ne")
    
    def start_round(self):
        
        if self.current_round < len(self.coordinates):
            coord = self.coordinates[self.current_round]
            self.current_round += 1
            
            place_name = coord["name"]
            position_name  =self.current_round*10
            self.map_draw.text(xy=(100,position_name+50),text=f'Find {place_name}',fill="black" )
            self.map_image_tk = ImageTk.PhotoImage(self.map_image)
            self.image_label.configure(image=self.map_image_tk)
            
            guess_x, guess_y = self.get_user_guess(place_name)
            actual_x, actual_y = coord["x"], coord["y"]
            with open(f"{script_dir}\\stored_score.txt","a") as score:
                score.write(f"{guess_x},{guess_y},{actual_x},{actual_y},{place_name}\n")

            self.draw_dot_with_label(guess_x, guess_y, f"Guess : {place_name}")
            
            self.start_round()
        else:
            self.display_final_results()
            result_window = ctk.CTkToplevel(self.root)
            result_window.title("Results")
               
            box = ctk.CTkTextbox(result_window)
            box.pack(fill="both", expand=True, padx=10, pady=10)
            with open(f"{script_dir}\\stored_score.txt","r") as scores:
               score_ = scores.read().split("\n")
               for score__ in score_:
                check= score__.split(",")
                if check[0] != "":
                    print(check[0])
                    box.insert("end",self.show_results(int(check[0]),int(check[1]),int(check[2]),int(check[3]),str(check[4])))
                else:
                    
                    erase = open(f"{script_dir}\\stored_score.txt","w")
            button = ctk.CTkButton(result_window,text="OK !",command=lambda : result_window.destroy()).pack()

    def display_final_results(self):
        for coord in self.coordinates:
            self.draw_dot_with_label(coord["x"], coord["y"], coord["name"])
        # time.sleep(1)
        messagebox.showinfo("Game Over", "You have completed all rounds!")

    def get_user_guess(self, place_name):
        time.sleep(0.1)
        ctk.CTk.bell = lambda:None
        SilentMessageBox.showinfo("Your Turn", f"Locate the place: {place_name}")
        self.image_label.bind("<Button-1>", self.get_guess_click)
        self.guess_event.set("")
        self.root.wait_variable(self.guess_event)
        return self.guess_x, self.guess_y

    def get_guess_click(self, event):
        self.guess_x, self.guess_y = event.x, event.y
        self.guess_event.set("clicked")
    global place_name_
    def show_results(self, guess_x, guess_y, actual_x, actual_y, place_name_):
        
        
        # time.sleep(1)
        # messagebox.showinfo("Round Result", f"Place: {place_name_}\nYour Guess: ({guess_x}, {guess_y})\nActual: ({actual_x}, {actual_y})")
        return f"Place: {place_name_}\nYour Guess: ({guess_x}, {guess_y})\nActual: ({actual_x}, {actual_y})\n"
    def save_presets(self):
        with open(f"{script_dir}\\presets.json", "w") as f:
            json.dump(self.presets, f)

    def load_presets(self):
        if os.path.exists("presets.json"):
            with open(f"{script_dir}\\presets.json", "r") as f:
                self.presets = json.load(f)

    def reset_presets(self):
        if messagebox.askyesno("Reset Presets", "Are you sure you want to clear all presets?"):
            self.presets.clear()
            self.save_presets()
            messagebox.showinfo("Presets Reset", "All presets have been cleared.")


    def toggle_dark_mode(self):
        if self.dark_mode_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def upload_preset(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                new_presets = json.load(f)
                self.presets.update(new_presets)
                self.save_presets()
                messagebox.showinfo("Upload Successful", "Presets from the selected file have been added.")
    
    
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("900x700")
    app = MapGameApp(root)
    root.mainloop()
