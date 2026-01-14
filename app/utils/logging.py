from colorama import init, Fore

init(autoreset=True)

class Logger:
    @classmethod
    def info(cls, message: str) -> None:
        print(Fore.BLUE + "INFO:\t  " + message)

    @classmethod
    def success(cls, message: str) -> None:
        print(Fore.GREEN + "SUCCESS:  " + message)

    @classmethod
    def warn(cls, message: str) -> None:
        print(Fore.YELLOW + "WARNING:  " + message)

    @classmethod
    def error(cls, message: str) -> None:
        print(Fore.RED + "ERROR:\t  " + message)