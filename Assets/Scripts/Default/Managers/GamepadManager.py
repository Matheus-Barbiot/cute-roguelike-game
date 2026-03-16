#icon=SCRIPTWIN
from bge import logic


class Gamepad:
    """
    Gamepad helper class built on top of `bge.logic.joystick`.

    This class simplifies gamepad input handling and is especially suited
    for menu navigation (e.g. Menu component in logic_menu.py).

    [IMPORTANT]
    The button MAP may vary depending on the specific gamepad model
    and driver configuration.

    [TODO]
    Allow custom button mapping instead of using a fixed default map.
    """

    MAP = {
        "a": 0, "b": 1, "x": 2, "y": 3,
        "back": 4, "analog": 5, "start": 6,
        "l3": 7, "r3": 8,
        "lb": 9, "rb": 10,
        "up": 11, "down": 12, "left": 13, "right": 14
    }

    def __init__(self, index=0, deadzone=0.2):
        self.index = index
        self.deadzone = deadzone
        self.active_joy = None

        # State memory for edge detection
        self.last_frame = set()
        self.current_frame = set()

        self._find_joystick()

        # Ensure automatic updates even if the joystick is unplugged/replugged
        logic.getCurrentScene().pre_draw.append(self._auto_update)

    def _find_joystick(self):
        """Try to find and activate a connected joystick."""
        try:
            joys = logic.joysticks
            if self.index < len(joys) and joys[self.index]:
                self.active_joy = joys[self.index]
                print(f"[Gamepad] '{self.active_joy.name}' connected.")
                return True
        except Exception:
            pass

        self.active_joy = None
        return False

    def _auto_update(self):
        """
        Internal update method.
        Handles hot-plugging and safe state reset when the joystick is removed.
        """
        if not self.active_joy:
            if not self._find_joystick():
                self.current_frame.clear()
                return

        try:
            current_buttons = self.active_joy.activeButtons
            self.last_frame = self.current_frame.copy()
            self.current_frame = set(current_buttons)

        except (AttributeError, RuntimeError, Exception):
            # Joystick was likely disconnected
            self.active_joy = None
            self.current_frame.clear()
            self.last_frame.clear()

    def _decode_button(self, input_val):
        """Convert a button name or index into a numeric button ID."""
        if isinstance(input_val, int):
            return input_val
        if isinstance(input_val, str):
            return self.MAP.get(input_val.lower())
        return None

    # --- Public API ---

    # Buttons
    def hold(self, btn):
        """Return True while the button is being held."""
        if not self.active_joy:
            return False

        idx = self._decode_button(btn)
        return idx in self.current_frame if idx is not None else False

    def pressed(self, btn):
        """Return True only on the frame the button is pressed."""
        if not self.active_joy:
            return False

        idx = self._decode_button(btn)
        return (
            idx in self.current_frame and idx not in self.last_frame
            if idx is not None else False
        )

    def released(self, btn):
        """Return True only on the frame the button is released."""
        if not self.active_joy:
            return False

        idx = self._decode_button(btn)
        return (
            idx in self.last_frame and idx not in self.current_frame
            if idx is not None else False
        )

    # Analog sticks
    def get_axis(self, side="left", axis="x"):
        """
        Get the analog stick axis value.

        :param side: 'left' or 'right'
        :param axis: 'x' or 'y'
        :return: float in range [-1.0, 1.0], deadzone applied
        """
        if not self.active_joy:
            return 0.0

        offset = 2 if str(side).lower() in ("right", "r") else 0
        idx = 1 if str(axis).lower() in ("y", "vertical", "1") else 0

        try:
            val = self.active_joy.axisValues[offset + idx]
            if abs(val) < self.deadzone:
                return 0.0
            return -val if idx == 1 else val
        except Exception:
            return 0.0

    # D-pad
    def dpad(self, direction):
        """Return True if the given D-pad direction is active."""
        if not self.active_joy:
            return False

        direction = direction.upper()
        values = {"UP": 11, "DOWN": 12, "LEFT": 13, "RIGHT": 14}

        try:
            return values.get(direction) in self.current_frame
        except Exception:
            return False