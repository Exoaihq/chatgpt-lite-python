from typing import Any, Tuple
import asyncio

class FullScreen:
    def __init__(self):
        self.full_screen = False
        self.doc_elm_ref = None

    async def toggle_full_screen(self):
        if self.full_screen:
            await self.exit_full_screen()
        else:
            await self.request_full_screen()

    async def request_full_screen(self):
        # Implement request full screen functionality here
        self.full_screen = True

    async def exit_full_screen(self):
        # Implement exit full screen functionality here
        self.full_screen = False

    async def full_screen_change_handle(self):
        # Implement full screen change event handling here
        self.full_screen = not self.full_screen

    async def keydown_f11_handle(self, e: Any):
        if e.key == 'F11':
            await self.toggle_full_screen()
            e.stopPropagation()
            e.preventDefault()

    async def add_event_listeners(self):
        # Implement adding event listeners for fullscreenchange and keydown events here
        pass

    async def remove_event_listeners(self):
        # Implement removing event listeners for fullscreenchange and keydown events here
        pass

def use_full_screen() -> Tuple[bool, FullScreen]:
    full_screen = FullScreen()
    asyncio.run(full_screen.add_event_listeners())
    return full_screen.full_screen, full_screen.toggle_full_screen