from mailtm import Email # temp mail
import time # for delays
import random
import string
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import tkinter as tk # for the GUI
import random
from PIL import Image, ImageTk

# Refer a Friend (RaF) Palia


def run(playwright: Playwright, email, username, password, url) -> None:
    browser = playwright.chromium.launch(headless=False) # True if u wanna see everything
    context = browser.new_context()
    page = context.new_page()

    all_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    all_countries = ["Sweden", "United States", "Åland Islands", "Bolivia", "Brazil", "Cambodia"]

    year = str(random.randint(1970, 2004))
    month = random.choice(all_months)
    day = str(random.randint(1, 28))
    country = "Sweden" #random.choice(all_countries) # TODO: Make it work with more countries.
    #region = "swe"

    page.goto(url)
    page.get_by_placeholder("einar@palia.com").click()
    page.get_by_placeholder("einar@palia.com").fill(email)

    page.get_by_placeholder("EinarLovesPebbles11").click()
    page.get_by_placeholder("EinarLovesPebbles11").fill(username)

    page.get_by_placeholder("New Password").click()
    page.get_by_placeholder("New Password").fill(password)

    page.get_by_placeholder("Confirm Password").click()
    page.get_by_placeholder("Confirm Password").fill(password)

    page.get_by_placeholder("Month").click()
    page.get_by_role("option", name=month).click()
    page.get_by_placeholder("Day").click()
    page.get_by_role("option", name=day, exact=True).click()
    page.get_by_placeholder("Year").click()
    page.get_by_role("option", name=year).click()
    page.locator("#vs1__combobox div").first.click()
    #page.get_by_placeholder("Country / Region").fill(region)
    page.get_by_role("option", name=country).click()

    page.get_by_label("Check this box to get email").check()
    page.get_by_label("I agree to the Terms of").check()

    page.get_by_role("button", name="Submit").click()

    time.sleep(5) # To check if it has actually submitted it.

    # ---------------------
    context.close()
    browser.close()


def listener(message):
    print("\nSubject: " + message['subject'])
    print("Content: " + message['text'] if message['text'] else message['html'])


def temp_mail():
    try: 
        test = Email()
        # Make new email address
        test.register()
        email = str(test.address)
        return email
    except:
        email = random_username(15) + "@gmail.com"
        return email

    # test.start(listener)
    # test.stop

# Very bad looking usernames
def random_username(max_characters):
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(characters) for _ in range(max_characters))
    return username


# WARNING: Not a suitable password generator.
# This is not for strong password but just for throwaway passwords.
def random_password(length_of_password):
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '[', ']', '{', '}', '|', ';', ':', "'", '"', ',', '.', '<', '>', '?', '/']
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    print(lowercase_letters)
    all_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # Ensure at least one special character, one lowercase letter, and one uppercase letter, one number
    password = [random.choice(special_characters),
                random.choice(lowercase_letters),
                random.choice(uppercase_letters),
                random.choice(all_numbers)] # Might not work with the all_numbers, havent tested it.
     # Generate the rest of the password randomly
    remaining_length = length_of_password - len(password)
    all_characters = special_characters + list(lowercase_letters) + list(uppercase_letters) + list(string.digits)  # Include digits as well if needed

    for _ in range(remaining_length):
        password.append(random.choice(all_characters))

    # Shuffle the characters to make it more random
    random.shuffle(password)

    # Convert the list to a string
    password_str = ''.join(password)

    return password_str


def create_referral_code_url(input_strings):
    pattern = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
    #match = re.search(pattern, input_strings) # For ONE pattern
    matches = pattern.findall(input_strings)
    urls = []
    #print(matches)

    if matches:
        matches = set(matches) # Removes any duplicates.
        for match in matches:
            #print(match)
            url = "https://accounts.palia.com/sign-up?referral=" + match
            urls.append(url)
    return urls


def palia_raf(url):
    raf_urls = create_referral_code_url(url)
    if raf_urls is not None:
        with sync_playwright() as playwright:
            for raf_url in raf_urls:
                #print("URL: ", raf_url)
                for i in range(5):
                    #global raf_counter
                    #raf_counter += 1
                    email = temp_mail()
                    username = random_username(20) #+ str(i)
                    password = random_password(15) #'6n*"37Hnt3+q'
                    #print(email)
                    #print(username)
                    #print(password)
                    time.sleep(1)
                    run(playwright, email, username, password, raf_url) # Need to add URL
    else:
        pass
# GUI

class MyGUI:
    def __init__(self):
        self.root = tk.Tk() #start
        self.is_dark_mode = True
        self.light_mode = {
            'bg': 'white',
            'fg': 'black',
            'entry_bg': '#eee',
            'entry_fg': 'black',
            'btn_bg': '#ddd',
            'btn_fg': 'black'
        }
        self.is_dark_mode = {
            'bg': '#333',
            'fg': 'white',
            'entry_bg': '#555',
            'entry_fg': 'white',
            'btn_bg': '#444',
            'btn_fg': 'white'
        }



        self.root.geometry("550x500")
        self.root.title("RAF Palia")
        #self.root.iconbitmap("chapaa.ico") #TODO: _tkinter.TclError: bitmap "chapaa.ico" not defined
        #im = Image.open('squirrels.png')
        #photo = ImageTk.PhotoImage(im)
        #self.root.wm_iconphoto(True, photo)
        #self.root.config(bg="#26242f")
        self.root.eval('tk::PlaceWindow . center')

        self.label = tk.Label(self.root, text="Recruit a Friend for Palia", font=("Arial", 18))
        self.label.pack(padx=10, pady=10)

        self.label_explain = tk.Label(self.root, text="This app creates 5 accounts that then use your recruit-a-friend code(s).", font=("Arial", 12))
        self.label_explain.pack()
        self.label_explain_two = tk.Label(self.root, text="So you get all the chapaa rewards.", font=("Arial", 12))
        self.label_explain_two.pack(pady=10)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 12))
        self.textbox.pack(padx=10)

        self.button = tk.Button(self.root, text="Start", font=("Arial", 18), command=self.show_message)
        self.button.pack(padx=20, pady=20)

        self.label_progress = tk.Label(self.root, text="Status", font=("Arial", 16))
        self.label_progress.pack(padx=20, pady=20)

        self.root.mainloop() #end

    def apply_theme(self, theme):
        self.root.config(bg = theme['bg'])
        for widget in self.root.winfo_children():
            widget_type = widget.winfo_class()

            if widget_type == 'Label':
                widget.config(bg=theme['bg'], fg=theme['fg'])
            #elif widget_type == 'Entry':
    

    def show_message(self): # When you click the button
        all_raf = self.textbox.get("1.0", tk.END)
        self.label_progress.config(text="Please wait...")
        self.root.after(50, lambda: self.process_and_update_label(all_raf))

    def process_and_update_label(self, all_raf):
        palia_raf(all_raf)
        self.label_progress.config(text="Completed. Restart Palia & check news!")


def main():
    #test_url = "https://accounts.palia.com/sign-up?referral=28bc7cde-331b-4216-a6c8-78d12f8fed8f"
    MyGUI()
    #print(random_password(15))



if __name__ == '__main__':
    main()