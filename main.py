from mailtm import Email # temp mail
import time # for delays
import random
import string
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import tkinter as tk # for the GUI
import threading


# Refer a Friend (RaF) Palia

raf_counter = 0


def run(playwright: Playwright, email, username, password, url) -> None:
    browser = playwright.chromium.launch(headless=False) # True if u wanna see everything
    context = browser.new_context()
    page = context.new_page()

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
    page.get_by_role("option", name="January").click()
    page.get_by_placeholder("Day").click()
    page.get_by_role("option", name="1", exact=True).click()
    page.get_by_placeholder("Year").click()
    page.get_by_role("option", name="1990").click()
    page.locator("#vs1__combobox div").first.click()
    page.get_by_placeholder("Country / Region").fill("swe")
    page.get_by_role("option", name="Sweden").click()

    page.get_by_label("Check this box to get email").check()
    page.get_by_label("I agree to the Terms of").check()

    page.get_by_role("button", name="Submit").click()

    time.sleep(5)

    # ---------------------
    context.close()
    browser.close()


def listener(message):
    print("\nSubject: " + message['subject'])
    print("Content: " + message['text'] if message['text'] else message['html'])


def temp_mail():
    #TODO: If it dosent work, create a fake email. Maybe it will also work.
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
    # Ensure at least one special character, one lowercase letter, and one uppercase letter
    password = [random.choice(special_characters),
                random.choice(lowercase_letters),
                random.choice(uppercase_letters)]
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
    #match = re.search(pattern, input_strings)
    matches = pattern.findall(input_strings)
    urls = []
    print(matches)

    if matches:
        matches = set(matches)
        for match in matches:
            print(match)
            url = "https://accounts.palia.com/sign-up?referral=" + match
            urls.append(url)
    return urls

"""     # Check if the pattern is found
    if match:
        # If found, get the matched string using group(0)
        matched_pattern = match.group(0)
        url = "https://accounts.palia.com/sign-up?referral=" + matched_pattern
        
        # Now you can use the matched pattern as needed
        print("Pattern found:", matched_pattern)
    else:
        print("Pattern not found.")
    return url """


def palia_raf(url):
    raf_urls = create_referral_code_url(url)
    if raf_urls is not None:
        with sync_playwright() as playwright:
            for raf_url in raf_urls:
                print("URL: ", raf_url)
                for i in range(5):
                    global raf_counter
                    raf_counter += 1
                    #email = temp_mail()
                    username = random_username(20) #+ str(i)
                    password = random_password(15) #'6n*"37Hnt3+q'
                    #print(email)
                    print(username)
                    print(password)
                    time.sleep(2)
                    #run(playwright, email, username, password, raf_url) # Need to add URL
    else:
        print("Wrong URL.")

# TODO:
# Create a GUI (Tkinter is okey)
# Make a textbox
# Make it work with a list of referral codes.
        
# GUI
""" root = tk.Tk()

root.geometry("500x500")
root.title("RAF Palia")

label = tk.Label(root, text="Hello World", font=("Arial", 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=5, font=("Arial", 16))
textbox.pack(padx=10)

button = tk.Button(root, text="Click", font=("Arial", 18))
button.pack()

# maybe not use this.
#myentry = tk.Entry(root)
#myentry.pack()

root.mainloop() """

progress_counter = "Progress..."

class MyGUI:
    def __init__(self):
        self.root = tk.Tk() #start

        self.label = tk.Label(self.root, text="Recruit a Friend Palia", font=("Arial", 18))
        self.label.pack(padx=20, pady=20)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 16))
        self.textbox.pack(padx=10)

        self.button = tk.Button(self.root, text="Click", font=("Arial", 18), command=self.show_message)
        self.button.pack()

        self.label_progress = tk.Label(self.root, text="Status", font=("Arial", 16))
        self.label_progress.pack(padx=20, pady=20)

        self.root.mainloop() #end

    def show_message(self):
        all_raf = self.textbox.get("1.0", tk.END)
        self.label_progress.config(text="Please wait...")
        palia_raf(all_raf)
        self.root.after(50, lambda: self.label_progress.config(text="Completed."))


def main():
    print("Main")
    url = "https://accounts.palia.com/sign-up?referral=6c12dc58-f439-4291-9909-e4fef36cb237"
    MyGUI()
    #palia_raf(url)


if __name__ == '__main__':
    main()