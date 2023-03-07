print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, make_key
from kmk.matrix import DiodeOrientation
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.RGB import RGB
from midi import Midi

# KEYTBOARD SETUP
layers = Layers()
keyboard = KMKKeyboard()
encoders = EncoderHandler()
tapdance = TapDance()
mouse_keys = MouseKeys()
tapdance.tap_time = 150
keyboard.modules = [layers, encoders, tapdance, mouse_keys]

# SWITCH MATRIX
keyboard.col_pins = (board.D3, board.D4, board.D5, board.D6)
keyboard.row_pins = (board.D7, board.D8, board.D9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# ENCODERS
encoders.pins = ((board.A2, board.A1, board.A0, False), (board.SCK, board.MISO, board.MOSI, False),)

# EXTENSIONS
rgb_ext = RGB(pixel_pin = board.D10, num_pixels=4, hue_default=50)
midi_ext = Midi()
keyboard.extensions.append(rgb_ext)
keyboard.extensions.append(midi_ext)
keyboard.debug_enabled = False

#********* LAYERS *******
LAYER1 = KC.TO(0)
LAYER2 = KC.TO(1)
LAYER3 = KC.TO(2)

#******** Layer 1 *******
# MACROS ROW 1
UNDO_L3  = KC.TD(KC.LCMD(KC.Z), LAYER3)
DEL_LINE = KC.LCMD(KC.D)
SEL_ALL = KC.LCMD(KC.A)
REDO  = KC.LCMD(KC.Y)

# MACROS ROW 2
ALT_TAB_L2 = KC.TD(KC.LALT(KC.TAB), LAYER2)
CLEAR = simple_key_sequence([KC.LCMD(KC.LSFT(KC.BSPC))])
INSPECT = simple_key_sequence([KC.LCMD(KC.LALT(KC.I))])
BROWSER_PROD = simple_key_sequence([KC.LALT(KC.SPACE), KC.MACRO_SLEEP_MS(100), send_string('Google Chrome'),KC.ENTER, KC.LCMD(KC.T), KC.LCMD(KC.L), KC.MACRO_SLEEP_MS(100), send_string('https://ds-live.matic.sdm.network/admin'), KC.ENTER])

# MACROS ROW 3
ESCAPE_L1 = simple_key_sequence([KC.ESC, LAYER1])
MOUSE_LEFT_CLICK = KC.MB_LMB
PASTE = KC.LCMD(KC.V)
TD_PASTE_MUTE = KC.TD(PASTE, KC.MUTE)
LOCK = simple_key_sequence([KC.LCTRL(KC.LCMD(KC.Q)), KC.MACRO_SLEEP_MS(400), KC.ESCAPE])

ZOOM_IN = KC.LCMD(KC.EQUAL)
ZOOM_OUT = KC.LCMD(KC.MINUS)

# CUSTOM KEYS
def on_copy(*args, **kwargs):
    keyboard.tap_key(KC.LCMD(KC.C))
    return False #Returning True will follow thru the normal handlers sending the ALT key to the OS

MOUSE_LEFT_CLICK.after_release_handler(on_copy)

def on_layer1(*args, **kwargs):
    rgb_ext.set_rgb_fill((255, 0, 0))
    return False
LAYER1.after_release_handler(on_layer1)

def on_layer2(*args, **kwargs):
    rgb_ext.set_rgb_fill((0, 255, 0))
    return False
LAYER2.after_release_handler(on_layer2)

def on_layer3(*args, **kwargs):
    rgb_ext.set_rgb_fill((0, 0, 255))
    return False
LAYER3.after_release_handler(on_layer3)

#******** Layer 2 *******

_______ = KC.TRNS
xxxxxxx = KC.NO

# KEYMAPS

keyboard.keymap = [
    # Layer 1
    [
        ESCAPE_L1,  MOUSE_LEFT_CLICK, TD_PASTE_MUTE, LOCK,
        ALT_TAB_L2, CLEAR,            INSPECT,       BROWSER_PROD,
        UNDO_L3,    DEL_LINE,         SEL_ALL,       REDO,
    ],
    # Layer 2
    [
        ESCAPE_L1, xxxxxxx, xxxxxxx,
        xxxxxxx,   xxxxxxx, xxxxxxx,
        xxxxxxx,   xxxxxxx, xxxxxxx,
    ],
    # Layer 3
    [
        ESCAPE_L1, xxxxxxx, xxxxxxx,
        xxxxxxx,   xxxxxxx, xxxxxxx,
        xxxxxxx,   xxxxxxx, xxxxxxx,
    ]
]

encoders.map = [
                 ((KC.VOLD, KC.VOLU, KC.MUTE),  (ZOOM_OUT, ZOOM_IN, KC.RGB_TOG)),
                 ((KC.VOLD, KC.VOLU, KC.MUTE),  (ZOOM_OUT, ZOOM_IN, KC.RGB_TOG)),
                 ((KC.VOLD, KC.VOLU, KC.MUTE ), (ZOOM_OUT, ZOOM_IN, KC.RGB_TOG)),
                ]


if __name__ == '__main__':
    keyboard.go()
