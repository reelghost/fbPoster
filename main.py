import os
import sys
import glob
import shutil
from dotenv import load_dotenv, set_key
import customtkinter as ctk  # CustomTkinter for the GUI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import utils
import fbPoster
import instaPoster
import xPoster

# Load environment variables
load_dotenv()

class IhaPosterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ISWK Image Auto-Poster")
        self.geometry("700x600")
        
        # Check if .env exists to change button behavior
        self.env_exists = os.path.exists(".env")

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=20)

        # Facebook Email Label and Entry
        email_label = ctk.CTkLabel(input_frame, text="Facebook Email:", font=("Arial", 14))
        email_label.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")
        self.email_entry = ctk.CTkEntry(input_frame, width=220)
        self.email_entry.grid(row=1, column=0, padx=10, pady=5)

        # Facebook Password Label and Entry
        password_label = ctk.CTkLabel(input_frame, text="Facebook Password:", font=("Arial", 14))
        password_label.grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")
        self.password_entry = ctk.CTkEntry(input_frame, width=220, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Instagram Email Label and Entry
        insta_email_label = ctk.CTkLabel(input_frame, text="Instagram Email:", font=("Arial", 14))
        insta_email_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        self.insta_email_entry = ctk.CTkEntry(input_frame, width=220)
        self.insta_email_entry.grid(row=3, column=0, padx=10, pady=5)

        # Instagram Password Label and Entry
        insta_password_label = ctk.CTkLabel(input_frame, text="Instagram Password:", font=("Arial", 14))
        insta_password_label.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="w")
        self.insta_password_entry = ctk.CTkEntry(input_frame, width=220, show="*")
        self.insta_password_entry.grid(row=3, column=1, padx=10, pady=5)

        # x Email Label and Entry
        x_email_label = ctk.CTkLabel(input_frame, text="X Email:", font=("Arial", 14))
        x_email_label.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")
        self.x_email_entry = ctk.CTkEntry(input_frame, width=220)
        self.x_email_entry.grid(row=5, column=0, padx=10, pady=5)

        # x Password Label and Entry
        x_password_label = ctk.CTkLabel(input_frame, text="X Password:", font=("Arial", 14))
        x_password_label.grid(row=4, column=1, padx=10, pady=(0, 5), sticky="w")
        self.x_password_entry = ctk.CTkEntry(input_frame, width=220, show="*")
        self.x_password_entry.grid(row=5, column=1, padx=10, pady=5)

        images_folder_label = ctk.CTkLabel(input_frame, text="Images Folder Path:", font=("Arial", 14))
        images_folder_label.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="w")
        self.images_folder_entry = ctk.CTkEntry(input_frame, width=220)
        self.images_folder_entry.grid(row=7, column=0, padx=10, pady=5)

        posted_folder_label = ctk.CTkLabel(input_frame, text="Posted Images Folder Path:", font=("Arial", 14))
        posted_folder_label.grid(row=6, column=1, padx=10, pady=(0, 5), sticky="w")
        self.posted_folder_entry = ctk.CTkEntry(input_frame, width=220)
        self.posted_folder_entry.grid(row=7, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Captions Folder Path:", font=("Arial", 14)).pack(pady=2)
        self.captions_folder_entry = ctk.CTkEntry(self, width=300)
        self.captions_folder_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Sleep Interval (seconds):", font=("Arial", 14)).pack(pady=2)
        self.sleep_entry = ctk.CTkEntry(self, width=300)
        self.sleep_entry.pack(pady=5)
        
        self.save_button = ctk.CTkButton(self, text="Save Settings" if not self.env_exists else "Edit Settings", command=self.save_settings)
        self.save_button.pack(pady=10)

        self.run_button = ctk.CTkButton(self, text="Run Auto-Poster", command=self.run_script)
        self.run_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # Preload existing settings if .env exists
        if self.env_exists:
            self.load_settings()

    def save_settings(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        insta_email = self.insta_email_entry.get()
        insta_password = self.insta_password_entry.get()
        x_email = self.x_email_entry.get()
        x_password = self.x_password_entry.get()
        images_folder = self.images_folder_entry.get()
        posted_folder = self.posted_folder_entry.get()
        captions_folder = self.captions_folder_entry.get()
        sleep_interval = self.sleep_entry.get()

        # Save to .env file
        set_key(".env", "FB_EMAIL", email)
        set_key(".env", "FB_PASS", password)
        set_key(".env", "INSTA_EMAIL", insta_email)
        set_key(".env", "INSTA_PASS", insta_password)
        set_key(".env", "X_EMAIL", x_email)
        set_key(".env", "X_PASS", x_password)
        set_key(".env", "IMAGES_FOLDER", images_folder)
        set_key(".env", "POSTED_FOLDER", posted_folder)
        set_key(".env", "CAPTIONS_FILE", captions_folder)
        set_key(".env", "SLEEP_INTERVAL", sleep_interval)

        self.status_label.configure(text="Settings saved successfully!", text_color="green")

    def load_settings(self):
        self.email_entry.insert(0, os.getenv("FB_EMAIL", ""))
        self.password_entry.insert(0, os.getenv("FB_PASS", ""))
        self.insta_email_entry.insert(0, os.getenv("INSTA_EMAIL", ""))
        self.insta_password_entry.insert(0, os.getenv("INSTA_PASS", ""))
        self.x_email_entry.insert(0, os.getenv("X_EMAIL", ""))
        self.x_password_entry.insert(0, os.getenv("X_PASS", ""))
        self.images_folder_entry.insert(0, os.getenv("IMAGES_FOLDER", ""))
        self.posted_folder_entry.insert(0, os.getenv("POSTED_FOLDER", ""))
        self.captions_folder_entry.insert(0, os.getenv("CAPTIONS_FILE", ""))
        self.sleep_entry.insert(0, os.getenv("SLEEP_INTERVAL", ""))
    
    def get_user_input(self, prompt):
        """Function to get user input using a modal popup."""
        input_window = ctk.CTkToplevel(self)
        input_window.title("Fb Input")
        input_window.geometry("300x200")
        input_window.grab_set()  # Make it modal

        # Label to show the prompt
        ctk.CTkLabel(input_window, text=prompt, font=("Arial", 14)).pack(pady=10)

        # Entry widget for user input
        user_input_entry = ctk.CTkEntry(input_window, width=300)
        user_input_entry.pack(pady=10)

        # Variable to store the input
        user_input = ctk.StringVar()

        def submit():
            user_input.set(user_input_entry.get())
            input_window.destroy()  # Close the popup

        # Button to submit input
        ctk.CTkButton(input_window, text="Submit", command=submit).pack(pady=20)

        # Wait for the input window to close
        input_window.wait_window()

        return user_input.get()  # Return the user's input


    def run_script(self):
        self.status_label.configure(text="Running the auto-poster...", text_color="blue")
        self.update()  # Refresh GUI
        
        # Pass the current instance to the main function
        import threading
        threading.Thread(target=lambda: main(self)).start()
        self.status_label.configure(text="Process started...", text_color="green")


def get_caption(media_path, captions_file="captions.txt"):
    """
    Get the caption for an image based on its file name's number.
    """
    try:
        file_name = os.path.basename(media_path)
        file_number = int(os.path.splitext(file_name)[0])
        with open(captions_file, "r", encoding="utf-8") as file:
            captions = file.readlines()

        if file_number <= 0 or file_number > len(captions):
            return f"Error: No caption for file number {file_number}."
        
        caption = captions[file_number - 1].strip()  # Remove any extra whitespace or newline
        return caption
    except ValueError:
        return f"Error: File name '{file_name}' does not contain a valid number."
    except FileNotFoundError:
        return f"Error: Captions file '{captions_file}' not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# Updated main function:
def main(gui_instance):
    IMAGES_FOLDER = os.getenv("IMAGES_FOLDER")
    CAPTIONS_FILE = os.getenv("CAPTIONS_FILE")
    SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL"))
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROFILE_PATH = os.path.join(BASE_DIR, 'chrome_profile')

    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-geolocation")
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,  # Disable password manager
        'profile.password_manager_enabled': False  # Disable password saving prompt
    })
    options.add_argument(f"--user-data-dir={PROFILE_PATH}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    while True:  # Infinite loop
        media = utils.get_first_image_path(IMAGES_FOLDER)
        if media is None:
            gui_instance.status_label.configure(text="No images found. Exiting...", text_color="red")
            break  # Exit the loop if no images are found
        caption = get_caption(media, CAPTIONS_FILE)
        # Facebook
        fbPoster.fb_main(driver=driver, media=media, caption=caption, gui_instance=gui_instance)
        # # Instagram
        instaPoster.insta_main(driver=driver, media=media, caption=caption, gui_instance=gui_instance)
        # # x.com
        xPoster.x_main(driver, media, caption, gui_instance)

        
        # move image
        utils.move_image_to_posted(media)
        # Wait before processing the next image
        sleep(SLEEP_INTERVAL)
    
    driver.quit()


if __name__ == "__main__":
    app = IhaPosterGUI()
    app.mainloop()
