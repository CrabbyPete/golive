import asyncio
from bleak import BleakScanner


async def main():
    stop_event = asyncio.Event()

    # TODO: add something that calls stop_event.set()
    devices = {}

    def callback(device, advertising_data):
        if "Flic" in device.name:
            if not device.name in devices.keys():
                print(device.name)
                devices[device.name] = device.address

    async with BleakScanner(callback) as scanner:
        ...
        # Important! Wait for an event to trigger stop, otherwise scanner
        # will stop immediately.
        await stop_event.wait()

    # scanner stops when block exits
    ...

asyncio.run(main())