from venv import create
from pokedex.gui import *

IMAGE = None


def main(async_loop):
    window = createWindow()
    window.title("Pokedex")
    addSearchBar(window, async_loop)
    window.mainloop()


if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()
    main(async_loop)
