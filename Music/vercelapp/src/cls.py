import os

from src.banner import banner


def cls():
    os.system("cls" if os.name == "nt" else "clear")
    banner()
