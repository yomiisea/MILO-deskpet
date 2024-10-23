# aswitch.py Switch and pushbutton classes for asyncio
# Delay_ms A retriggerable delay class. Can schedule a coro on timeout.
# Switch Simple debounced switch class for normally open grounded switch.
# Pushbutton extend the above to support logical state, long press and
# double-click events
# Tested on Pyboard but should run on other microcontroller platforms
# running MicroPython and uasyncio.

# The MIT License (MIT)
#
# Copyright (c) 2017 Peter Hinch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import uasyncio as asyncio
import utime as time
# Remove dependency on asyn to save RAM:
# launch: run a callback or initiate a coroutine depending on which is passed.
async def _g():
    pass
type_coro = type(_g())

# If a callback is passed, run it and return.
# If a coro is passed initiate it and return.
# coros are passed by name i.e. not using function call syntax.
def launch(func, tup_args):
    res = func(*tup_args)
    if isinstance(res, type_coro):
        loop = asyncio.get_event_loop()
        loop.create_task(res)


class Delay_ms(object):
    def __init__(self, func=None, args=(), can_alloc=True, duration=1000):
        self.func = func
        self.args = args
        self.can_alloc = can_alloc
        self.duration = duration  # Default duration
        self.tstop = None  # Not running
        self.loop = asyncio.get_event_loop()
        if not can_alloc:
            self.loop.create_task(self._run())

    async def _run(self):
        while True:
            if self.tstop is None:  # Not running
                await asyncio.sleep_ms(0)
            else:
                await self.killer()

    def stop(self):
        self.tstop = None

    def trigger(self, duration=0):  # Update end time
        if duration <= 0:
            duration = self.duration
        if self.can_alloc and self.tstop is None:  # No killer task is running
            self.tstop = time.ticks_add(time.ticks_ms(), duration)
            # Start a task which stops the delay after its period has elapsed
            self.loop.create_task(self.killer())
        self.tstop = time.ticks_add(time.ticks_ms(), duration)

    def running(self):
        return self.tstop is not None

    __call__ = running

    async def killer(self):
        twait = time.ticks_diff(self.tstop, time.ticks_ms())
        while twait > 0:  # Must loop here: might be retriggered
            await asyncio.sleep_ms(twait)
            if self.tstop is None:
                break  # Return if stop() called during wait
            twait = time.ticks_diff(self.tstop, time.ticks_ms())
        if self.tstop is not None and self.func is not None:
            launch(self.func, self.args)  # Timed out: execute callback
        self.tstop = None  # Not running

class Switch(object):
    debounce_ms = 50
    def __init__(self, pin):
        self.pin = pin # Should be initialised for input with pullup
        self._open_func = False
        self._close_func = False
        self.switchstate = se