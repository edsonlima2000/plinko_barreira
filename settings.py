from utils.colors import COLORS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60
TITLE = "Plinko com Barreira"

MAX_BALLS = 5
DEFAULT_BET = 3
SLOT_VALUES = [0, 1, 2, 3, 2, 1, 5]

TOP_PANEL_HEIGHT = 90
BOTTOM_PANEL_HEIGHT = 130

BOARD_X = 150
BOARD_Y = 105
BOARD_WIDTH = 700
BOARD_HEIGHT = 470

BALL_RADIUS = 11
BALL_SPEED = 260.0
BALL_RELEASE_DELAY = 0.18

PIN_RADIUS = 5
PIN_ROWS = 9
PIN_COLUMNS = 8

BARRIER_Y = BOARD_Y + BOARD_HEIGHT // 2
SLOT_HEIGHT = 85
SLOT_COUNT = len(SLOT_VALUES)
SLOT_TOP = BOARD_Y + BOARD_HEIGHT - SLOT_HEIGHT

STATUS_TEXT = {
    "MENU": "Clique em iniciar para preparar a rodada.",
    "SELECT_BET": "Escolha de 1 a 5 bolas e inicie a rodada.",
    "DROP_PHASE_1": "As bolas estao descendo ate a barreira.",
    "BARRIER_DECISION": "Clique nas bolas que deseja manter e confirme.",
    "DROP_PHASE_2": "As bolas mantidas seguem para os premios.",
    "ROUND_RESULT": "Rodada encerrada. Veja a soma dos premios.",
    "RESETTING": "Preparando nova rodada.",
}

UI = {
    "bg": COLORS["bg"],
    "panel": COLORS["panel"],
    "board_bg": COLORS["board_bg"],
    "board_border": COLORS["board_border"],
    "pin": COLORS["pin"],
    "barrier": COLORS["barrier"],
    "slot_line": COLORS["slot_line"],
    "slot_fill": COLORS["slot_fill"],
    "text": COLORS["text"],
    "muted": COLORS["muted"],
    "button": COLORS["button"],
    "button_hover": COLORS["button_hover"],
    "button_disabled": COLORS["button_disabled"],
    "button_text": COLORS["button_text"],
    "ball": COLORS["ball"],
    "ball_selected": COLORS["ball_selected"],
    "ball_abandoned": COLORS["ball_abandoned"],
    "ball_finished": COLORS["ball_finished"],
}
