from venv import create
from pokedex.gui import *


def main(async_loop):
    window = createWindow()
    addSearchBar(window, async_loop)
    window.mainloop()


if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()
    main(async_loop)
