import speech_recognition as sr
import keyboard
import mouse
import time

# Initialize recognizer
recognizer = sr.Recognizer()

# Voice commands mapped to keys
commands = {
    "move forward": "w", "go forward": "w", "walk": "w", "wow": "w", "warm": "w", "forward": "w", "no forward": "w", "move for": "w",
    "move back": "s", "go back": "s", "go backward": "s", "move backward": "s",
    "turn left": "a", "turn right": "d",
    "jump": "space", "jam": "space", "jumping": "space",
    "sprint": "shift", "crouch": "ctrl",
    "reload": "r",
    "enter": "enter", "select": "enter",
    "enter vehicle": "f", "exit vehicle": "f", "vehicle": "f",
    "honk": "e", "han": "e", "hon": "e", "on": "e",
    "brake": "s", "accelerate": "w",
    "look back": "c", "pause": "esc", "map": "m",
    "radio": "r", "interaction menu": "m",
    "mobile": "up", "phone up": "up",
    "mobile down": "down", "phone down": "down",
    "weapon": "tab", "change weapon": "q",
    "next weapon": "scrollup", "previous weapon": "scrolldown",
    "handbrake": "space",
    "change": "q", "change it": "q", "changing": "q",
    "back": "backspace",
    "shoot": "left_click", "fire": "left_click", "very bad": "left_click",
    "stop": "stop", "the shop": "stop", "release": "stop",
    "stop listening": "exit", "stop listen": "exit",
    "web": "shift",
    "accelerate": "right",
    "reverse": "left", "rivers": "left", "river": "left", "rever": "left",
    "aim": "right_click", "scope": "right_click",
    "m": "right_click",
    "veri good": "right_click",
}

def press_and_release(key, delay=0.1):
    keyboard.press(key)
    time.sleep(delay)
    keyboard.release(key)

def hold_and_release(key, hold_time):
    keyboard.press(key)
    time.sleep(hold_time)
    keyboard.release(key)

def recognize_speech():
    with sr.Microphone() as source:
        print("Calibrating microphone... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for commands...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                command = recognizer.recognize_google(audio, language="en-IN").lower()
                print(f"You said: {command}")

                if command in commands:
                    key = commands[command]

                    # Stop all keys and mouse
                    if key == "stop":
                        for k in ["w", "s", "a", "d", "shift", "ctrl", "space", "f", "r", "e", "enter", "tab", "esc", "up", "down", "c", "backspace", "q", "m", "left", "right"]:
                            keyboard.release(k)
                        mouse.release("left")
                        mouse.release("right")
                        print("Stopped all actions.")
                        continue

                    if key == "exit":
                        print("Exiting program.")
                        break

                    # Turn left/right logic
                    if command == "turn left":
                        keyboard.release("d")
                        keyboard.press("a")
                    elif command == "turn right":
                        keyboard.release("a")
                        keyboard.press("d")
                    elif command in ["left", "right"]:
                        if key == "right":
                            keyboard.release("left")
                        else:
                            keyboard.release("right")
                        keyboard.press(key)
                        time.sleep(2)
                        keyboard.release(key)
                    elif key == "web":
                        hold_and_release("shift", 3.0)
                    elif key in ["w", "s", "a", "d", "shift", "ctrl"]:
                        keyboard.press(key)
                    elif key in ["f", "r", "enter", "tab", "esc", "up", "down", "backspace", "q", "m"]:
                        press_and_release(key, 0.1)
                    elif key == "e":
                        press_and_release("e", 0.3)
                    elif key == "c":
                        press_and_release("c", 1.5)
                    elif key == "space":
                        press_and_release("space", 0.1 if command in ["jump", "jam", "jumping"] else 2.5)

                    # Arrow key logic (hold + opposite release)
                    elif key == "right":
                        keyboard.release("left")
                        keyboard.press("right")
                    elif key == "left":
                        keyboard.release("right")
                        keyboard.press("left")

                    # Right-click: Aim and hold
                    elif key == "right_click":
                        mouse.press("right")

                    # Left-click: Fire and hold (don't release automatically)
                    elif key == "left_click":
                        mouse.press("left")

            except sr.UnknownValueError:
                print("Could not understand the command.")
            except sr.RequestError:
                print("Could not connect to Google API. Check your internet connection.")

# Start the voice recognition loop
recognize_speech()
