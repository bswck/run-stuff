import asyncio
import atexit

asyncio.set_event_loop(loop := asyncio.new_event_loop())
loop.run_until_complete(asyncio.sleep(1))

print(loop)
atexit.register(lambda: print(asyncio.get_event_loop()))
