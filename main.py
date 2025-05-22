import time
import threading
from pynput import keyboard


class OneKeyBoard:
    def __init__(self) -> None:
        self.lane: str = ""
        self.last_symbol: str = ""
        self.key_pressed: bool = False
        self.underscore_printed: bool = False
        self.space_printed: bool = False
        self.press_start_time: float = 0.0
        
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
            self.key_pressed = False
            self.underscore_printed = False
            self.space_printed = False
            
    def check_hold_status(self):
        while True:
            if self.key_pressed and (not self.underscore_printed or not self.space_printed):
                if time.time() - self.press_start_time > 1:
                    self.lane = self.lane + self.last_symbol[:-1] + " "
                    self.last_symbol = ""
                    self.space_printed = True

                    print(f"\r{self.lane}", end="", flush=True)

                elif time.time() - self.press_start_time > 0.3:
                    self.last_symbol = self.last_symbol[:-1] + "_"
                    self.underscore_printed = True

                    print(f"\r{self.lane + self.last_symbol}", end="", flush=True)
            time.sleep(0.01)
    
    def main(self):
        threading.Thread(target=self.check_hold_status, daemon=True).start()
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == '__main__':
    OneKeyBoard().main()
