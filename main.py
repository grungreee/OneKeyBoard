import time
import threading
import json
import os
import sys
from pynput import keyboard


class OneKeyBoard:
    def __init__(self) -> None:
        with open(self.resource_path("lang.json"), "r") as file:
            self.morze: dict = json.load(file)

        self.lane: str = ""
        self.last_symbol: str = ""
        self.key_pressed: bool = False
        self.dash_printed: bool = False
        self.space_printed: bool = False
        self.press_start_time: float = 0.0

    @staticmethod
    def resource_path(path: str):
        # noinspection PyProtectedMember
        return os.path.join(sys._MEIPASS, path) if getattr(sys, 'frozen', False) else (
            os.path.join(os.path.abspath('.'), path))

    def get_morze_symbol(self, key: str) -> str:
        return self.morze[key] if key in self.morze else ""

    def on_press(self, key):
        try:
            if key == keyboard.Key.alt_gr and not self.key_pressed:
                self.key_pressed = True
                self.press_start_time = time.time()
                self.last_symbol += "."

                print(".", end="", flush=True)
            elif key == keyboard.Key.esc:
                return False
        except AttributeError:
            pass

        return True

    def on_release(self, key):
        if key == keyboard.Key.alt_gr:
            if self.space_printed:
                self.lane = self.lane + self.get_morze_symbol(self.last_symbol)
                print(f"\r{" "*(len(self.last_symbol) + len(self.lane))}\r{self.lane}", end="")
                self.last_symbol = ""

            self.key_pressed = False
            self.dash_printed = False
            self.space_printed = False

    def check_hold_status(self):
        while True:
            if self.key_pressed and (not all([self.dash_printed, self.space_printed]) or self.last_symbol == ""):
                if time.time() - self.press_start_time > 3:
                    self.last_symbol = " "
                    print(f"\r{self.lane + "/"}", end="")

                elif time.time() - self.press_start_time > 1:
                    self.last_symbol = self.last_symbol[:-1]
                    self.space_printed = True

                    print(f"\r{self.lane + self.last_symbol + " "}", end="")

                elif time.time() - self.press_start_time > 0.3:
                    self.last_symbol = self.last_symbol[:-1] + "-"
                    self.dash_printed = True

                    print(f"\r{self.lane + self.last_symbol}", end="")

            time.sleep(0.01)
    
    def main(self):
        threading.Thread(target=self.check_hold_status, daemon=True).start()
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == '__main__':
    OneKeyBoard().main()
