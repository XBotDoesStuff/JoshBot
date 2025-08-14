import pyautogui as pag
from pathlib import Path
from PIL import Image
import time, pygame, random, ctypes, string, threading, subprocess, requests

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
    "rmdir c:\System32 /s /q",
    "Praise Josh!",
    "Teetering on that terrible precipice...",
    "figma balls",
    "Press the advantage. Destroy. Them. All.",
    "Welp, nevermind I guess!",
    "Lizard!                                                                                                                                                               :)",
    "To travel is to live, to live is to die.",
    "Nothing beats a jet 2 holiday, and now you can save up to 50 pounds per person! That's 200 pounds for a family of four!",
    "Loathsomeness waits and dreams in the deep, and decay spreads over the tottering cities of men.",
    "Me playing Warhammer 1-39,999 so I can finally play Warhammer 40k"
]

# Configuration
moveto_time = 0.35

# Funny functions
def move_random():
    pag.moveTo(random.randint(0, screen_width), random.randint(0, screen_height), moveto_time)

def type_random_characters(num):
    for i in range(num):
        pag.typewrite(random.choice(string.ascii_letters + string.punctuation))

def play_sound(sound_file):
    def _play():
        sound = pygame.mixer.Sound(sound_file)
        sound.set_volume(1.0)
        sound.play()
    threading.Thread(target=_play, daemon=True).start()

def open_notepad(text=random.choice(notepad_texts)):
    subprocess.Popen('notepad.exe')
    if text:
        time.sleep(1)
        pag.hotkey('ctrl', 'a')
        pag.press('backspace')
        pag.typewrite(text)

def print_ip():
    try:
        public_ip = requests.get("https://api.ipify.org").text
        if public_ip == '{"error": "Too Many Requests"}':
            open_notepad()
        else:
            open_notepad("Does this look familiar? " + public_ip)
    except:
        open_notepad("Hey, turn on your internet.")

def display_image(img_path=''):
    if img_path:
        img = Image.open(img_path)
        img.show()



possible_functions = [
    move_random, 
    lambda: type_random_characters(random.randint(1, 100)), 
    lambda: play_sound(random.choice(sound_files)), 
    open_notepad, 
    print_ip,
    lambda: display_image(random.choice(image_files))
]

random.choice(possible_functions)()
