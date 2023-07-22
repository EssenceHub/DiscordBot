import keyboard
import time
import pydirectinput as input

class MouseCircler:
    circling = False
    circle_size = 5
    delay = 0

    def toggle_circling(self):
        self.circling = not self.circling
        if self.circling:
            print("Circling enabled")
        else:
            print("Circling disabled")

    def set_circle_size(self, size):
        self.circle_size = size
        print(f"Circle size set to {size}")

    def circle_mouse(self):
        while True:
            if self.circling:
                input.move(self.circle_size, 0)
                time.sleep(0.1)
                input.move(0, self.circle_size)
                time.sleep(0.1)
                input.move(-self.circle_size, 0)
                time.sleep(0.1)
                input.move(0, -self.circle_size)
                time.sleep(0.1)

mouse_circler = MouseCircler()
keyboard.add_hotkey('num 0', mouse_circler.toggle_circling)
keyboard.add_hotkey('num 1', lambda: mouse_circler.set_circle_size(10))
keyboard.add_hotkey('num 2', lambda: mouse_circler.set_circle_size(15))
keyboard.add_hotkey('num 3', lambda: mouse_circler.set_circle_size(20))

mouse_circler.circle_mouse()
