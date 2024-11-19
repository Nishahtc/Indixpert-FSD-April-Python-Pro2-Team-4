class bcolors:
    PURPLE = '\033[38;5;105m'
    TEAL = '\033[38;5;37m'
    ORANGE = '\033[38;5;214m'
    LIGHT_GREEN = '\033[38;5;118m'
    PINK = '\033[38;5;200m'
    RED = '\033[38;5;160m'
    WHITE_BOLD = '\033[1;97m'
    YELLOW_UNDERLINE = '\033[4;33m'
    GREY = '\033[38;5;240m'
    RESET = '\033[0m'
    LIGHT_YELLOW = '\033[38;5;229m'
    LIGHT_BLUE = '\033[38;5;39m'
    CYAN = '\033[38;5;51m'

    @staticmethod
    def colorize(text, color):
        return f"{color}{text}{bcolors.RESET}"
