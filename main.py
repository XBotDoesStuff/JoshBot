import pyautogui as pag
from pathlib import Path
from PIL import Image, ImageTk
import time, pygame, random, ctypes, string, threading, subprocess, requests, keyboard, os
from pywinauto import Application
import tkinter as tk

pygame.mixer.init()

# Gets the screen size of the primary display
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Path variables
sounds_folder = Path('sounds')
sound_files = [str(f).replace('\\', '/') for f in sounds_folder.glob("*") if f.suffix in [".mp3", ".wav", ".ogg"]]

images_folder = Path('images')
image_files = [str(f).replace('\\', '/') for f in images_folder.glob("*") if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".webp"]]

# Arrays
notepad_texts = [
    'DIE!',
    'CRUSH!',
    'JUDGEMENT!',
    'THY END IS NOW!',
    'I know where you live.',
    'We must aquire John.',
    "Bro we're operating on the same BRAINLENGTH!",
    "Have you heard of Sawcon? \n\n\n\n\n Sawcon deez nuts",
    "Overconfidence is a slow and insidious killer.",
    "In terms of coolness, Vaporeon is really cool...",
    r"""
&&&&&&@@*          *@@@&&&&&&&@&&&&&@&@@&&&&&&&&&&&&&&&@@&@@#              @@@@@
&@&@&@@#             .@@@@&@&@&@#%&@@@@@@@@@@@&@&@&@&@@&@%                 @@@@@
&&&@&@@                 @@&&&@@@@        .&@@&&&&&&@@@@/                   ,@&&&
&@&&&@*                   @@&@@&@&            &@&@@@&@                      @@@@
&&&&@@                      &@@@&@&              &@&@                       @@&&
&@&@@@                        %@@@&#*              .@&                      @@&&
&&&@@(                     %@(                                              @@&&
&@&@@(                    ****...     ..                                    @@@@
&&&&@@                                                                     .@&&&
&@&@@@.                                                                    (@@@@
&&&&@@@                                                                    @&@@@
&@&@&@@&                                        .**##&&&&&@@@&%(         .@@@@@@
&&&&&&@@&      &@@@@@@@@@@@@@@@@&             &@@@@@@@@     @(          /@&@@&&&
&@&@&@@&@@.     ,@.     @@@@@@@@@            .@@@@@@@@@      @*       (@&@&&&@&@
@@@@@&&@@&@%    @/      @@@@@@@@#            .@@@@@@@@@      #&   .@@@&&&&%@@&&&
@&@*    .***,  ,@       @@@@@@@@.             &@@@@@@@#      (&          .@@@@&@
&&&@@.         .@.      ,@@@@@@&               /@@@@@*       %&        ,@@&&&&&&
&@&&@&@@/       .@.       *@@@.   ,@@@&*                             &@@@&&@&@&@
&&&&&&@&@@  ,###/  **                                    (##.(#.     .@@@@&&&&&&
&@&@&@@@&     ,#(,                            .%,         .#.          *@&&@&@&@
&&&&&&@(                       @@%(&@%. .**//,                           &@&@&&&
&@&@@@*    .*%%#                                             /@@@@@@@@@@@&@&&@&@
&&&&&&&&&@@@@@@&@@@&/                                 .*&@@@&&@@@@@@@@@@@@&&&&&&
&@&@&@&@&@&@&@&@&@&@&@@%@@@&#*,                      #@&&@&@&@&@&@&@&@&@&@&@&@&@
&&&&&&&&&&&&&&&&&&&&&&&@#                             ,@&&&&&&&&&&&&&&&&&&&&&&&&
&@&@&@&@&@&@&@&@&@&@&@&&@@@&.                           @@@&&@&@&@&@&@&@&@&@&@&@
&&&&&&&&&&&&&&&&&&&&&&&&&&@,                             @@@&&&&&&&&&&&&&&&&&&&&
&@&@&@&@&@&@&@&@&@&@&@&&@,                                %@&@&@&@&@&@&@&@&@&@&@
&&&&&&&&&&&&&&&&&&&&@&&&@&@&@.                             &@@@&&&&&&&&&&&&&&&&&
&@&@&@&@&@&@&@&@&@&@&@&@@@&@,                               @@@@&@&@&@&@&@&@&@&@
&&&&&&&&&&&&&&&&&&&&&&&@@&@(                                ,@&&&&&&&&&&&&&&&&&&
&@&@&@&@&@&@&@&@&@&@&@&@@@@                                  %@@&@&@&@&@&@&@&@&@
-signed noftatty
    """,
    "sudo rm -rf --no-preserve-root /",
    r"""rmdir c:\System32 /s /q""",
    "Praise Josh!",
    "Teetering on that terrible precipice...",
    "figma balls",
    "Press the advantage. Destroy. Them. All.",
    "Welp, nevermind I guess!",
    "Lizard!                                                                                                                                                               :)",
    "To travel is to live, to live is to die.",
    "(Darling hold my hand!) Nothing beats a jet 2 holiday, and now you can save up to 50 pounds per person! That's 200 pounds for a family of four!",
    "Loathsomeness waits and dreams in the deep, and decay spreads over the tottering cities of men.",
    "Me playing Warhammer 1-39,999 so I can finally play Warhammer 40k",
    "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.",
    "We're always one step ahead :3 - XSCorporation",
    "Also try Terraria!",
    "Also try Minecraft!"
]

# Configuration
moveto_time = 0.35

min_wait_time = 180
max_wait_time = 300

# Utility functions
def kill_joshbot():
    print("Attempting to kill Joshbot")
    os._exit(0)

# Basic functions
def move_random():
    print("Moving cursor to random position")
    pag.moveTo(random.randint(0, screen_width), random.randint(0, screen_height), moveto_time)

def type_random_characters(num):
    print("Typing " + str(num) + " random characters")
    for i in range(num):
        pag.typewrite(random.choice(string.ascii_letters + string.punctuation))

def play_sound(sound_file):
    print("Playing sound: " + sound_file)
    def _play():
        sound = pygame.mixer.Sound(sound_file)
        length = sound.get_length()
        sound.set_volume(1.0)
        sound.play()
        time.sleep(length)
    threading.Thread(target=_play).start()

def open_notepad(text=random.choice(notepad_texts)):
    print("Messing with notepad: " + text)

    app = None
    notepad = None

    try:
        # Try to connect to existing Notepad
        app = Application(backend="uia").connect(title_re=".*Notepad")
        notepad = app.window(title_re=".*Notepad")
        print("Connected to existing Notepad.")
    except:
        # If not found, launch a new one
        print("No existing Notepad found. Launching a new one.")
        subprocess.Popen('notepad.exe')
        time.sleep(1)
        app = Application(backend="uia").connect(title_re=".*Notepad")
        notepad = app.window(title_re=".*Notepad")

    # Bring Notepad to focus
    notepad.set_focus()
    time.sleep(0.5)

    if text:
        pag.hotkey('ctrl', 'a')
        pag.press('backspace')
        pag.typewrite(text, interval=0.02)

def display_image(img_path=''):
    if not img_path:
        return

    root = tk.Tk()
    root.title("Image Viewer")
    root.attributes("-topmost", True)  # Bring window to front

    img = Image.open(img_path)
    tk_img = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=tk_img)
    label.pack()

    root.after(100, lambda: root.attributes("-topmost", False))  # Let user interact normally
    root.mainloop()

# Randomized basic functions (for the dictionary)
def random_characters():
    type_random_characters(random.randint(1, 100))

def random_sound():
    play_sound(random.choice(sound_files))

def random_basic_image():
    display_image(random.choice(image_files))

# Advanced functions
def print_ip():
    print("Printing IP")
    try:
        public_ip = requests.get("https://api.ipify.org").text
        if public_ip == '{"error": "Too Many Requests"}':
            open_notepad()
        else:
            open_notepad("Does this look familiar? " + public_ip)
    except:
        open_notepad("Hey, turn on your internet.")

def look_at_this_graph():
    print("Look at this graph!")
    display_image("special_images/lookatthisgraph.png")
    play_sound("special_sounds/lookatthisgraph.mp3")

def virtual_insanity():
    print("Dancing, walking, rearranging furniture.")
    beats = [0.46, 1.75, 3.27, 4.5, 5.89, 7.18, 8.49, 9.79, 11.07, 12.42, 13.72, 15, 16.33, 17.6]
    temp = 0
    threading.Thread(target=lambda: play_sound("special_sounds/virtual-insanity.mp3")).start()
    for i in range(len(beats)):
        wait_time = beats[i] - temp
        time.sleep(wait_time)
        print("sleeping for " + str(beats[i] - temp) + " seconds")
        temp = beats[i]
        display_image("special_images/Virtual-Insanity-Frames/" + str(i + 1) + ".png")

# Dictionary of possible outcomes for the random_function() function. Second value is weight, higher = more likely
possible_functions = {
    move_random: 4, 
    random_characters: 4, 
    random_sound: 4, 
    random_basic_image: 3,
    open_notepad: 3, 
    print_ip: 3,
    look_at_this_graph: 2,
    virtual_insanity: 2
}

def random_function():
    funcs, weights = zip(*possible_functions.items())
    function = random.choices(funcs, weights=weights, k=1)[0]
    function()

# ---------- MAIN PROGRAM ----------
keyboard.add_hotkey('ctrl+alt+j', kill_joshbot)
virtual_insanity()
"""while True:
    sleep_time = random.randint(min_wait_time, max_wait_time)
    print("Sleeping for " + str(sleep_time) + " seconds")
    time.sleep(sleep_time)
    threading.Thread(target=random_function).start()"""