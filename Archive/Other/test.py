import keyboard
import time

class KeySpammer:
    spamming = False
    
    def toggle_spamming(self):
        self.spamming = not self.spamming
        if self.spamming:
            print("Spamming enabled")
        else:
            print("Spamming disabled")

    def spam_e(self):
        while True:
            if self.spamming:
                keyboard.press('e')
                time.sleep(0.1)
                keyboard.release('e')
                time.sleep(0.1)

key_spammer = KeySpammer()
keyboard.add_hotkey('ctrl+f2', key_spammer.toggle_spamming)

key_spammer.spam_e()