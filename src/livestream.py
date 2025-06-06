import logging
import asyncio
import argparse

from pathlib                import Path
from open_gopro             import WirelessGoPro
from open_gopro.models      import proto, streaming
from open_gopro.util.logger import setup_logging, set_logging_level
from open_gopro.domain.exceptions import FailedToFindDevice

from oled   import OLED
from button import button
from config import settings
from get_network import get_network


# Start the OLED driver
oled = OLED()

async def main(ssid, password, url, args: argparse.Namespace):
    oled.write(["Searching", "for GOPRO"])
    setup_logging(__name__, args.log, {'bleak':logging.INFO})
    set_logging_level(logging.INFO)

    async with WirelessGoPro(
            args.identifier,
            enable_wifi=False,
            interfaces={WirelessGoPro.Interface.BLE},
            host_sudo_password='raspberry'
    ) as gopro:

        while True:
            oled.write(["Connecting", "to WiFi"])
            await gopro.access_point.connect(ssid, password)

            # Now wait for at button press to start streaming
            while gopro.is_http_connected:
                oled.write(["Waiting","for button"])
                await button()

                oled.write(["Streaming", "Now"])
                await gopro.streaming.start_stream(
                    streaming.StreamType.LIVE,
                    streaming.LivestreamOptions(
                        url=url,
                        minimum_bitrate=args.min_bit,
                        maximum_bitrate=args.max_bit,
                        starting_bitrate=args.start_bit,
                        resolution=args.resolution if args.resolution else None,
                        fov=args.fov if args.fov else None,
                        encode=args.encode,
                    ),
                )

                # Wait for a button press to stop streaming
                await button()
                oled.write(["Streaming","Stopped"])
                await gopro.streaming.stop_active_stream()

        await gopro.ble_command.release_network()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to the GoPro via BLE only, configure then start a Livestream, then display it with CV2."
    )
    parser.add_argument(
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. \
                If not used, first discovered GoPro will be connected to",
        default=None)

    parser.add_argument("--min_bit", type=int, help="Minimum bitrate.", default=1000)
    parser.add_argument("--max_bit", type=int, help="Maximum bitrate.", default=1000)
    parser.add_argument("--start_bit", type=int, help="Starting bitrate.", default=1000)

    parser.add_argument("--resolution", help="Resolution.",
                        choices=list(proto.EnumWindowSize.values()),
                        default=None,
                        type=int
                        )

    parser.add_argument("--fov",
                        help="Field of View.",
                        choices=list(proto.EnumLens.values()),
                        default=None,
                        type=int
                        )

    parser.add_argument("--encode",
                        help="Save video to sdcard.",
                        action=argparse.BooleanOptionalAction)

    parser.set_defaults(encode=True)

    parser.add_argument(
        "--log",
        type=Path,
        help="Location to store detailed log. Defaults to gopro_demo.log",
        default="gopro_demo.log",
    )


    parser.epilog = "Note that a minimal log is written to stdout. An extremely detailed log is written to the path set by the --log argument."
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    network, password = get_network()
    try:
        asyncio.run(main(network,
                         password,
                         settings['url'],
                         parse_arguments()))
    except FailedToFindDevice:
        oled.write(["Failed finding","device"])

