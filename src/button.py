import asyncio
from bleak import BleakClient

from log import log


async def button(address = "90:88:A9:50:41:94"):
    while True:
        try:
            async with BleakClient(address) as client:
                log.info("Button pressed")
                return True
        except Exception as e:
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(button())