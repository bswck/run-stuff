import asyncio

asyncio.set_event_loop(loop := asyncio.new_event_loop())
loop.run_until_complete(asyncio.sleep(1))
