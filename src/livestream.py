import logging
import asyncio
import argparse

from open_gopro             import WirelessGoPro
from open_gopro.models      import proto, streaming
from open_gopro.util        import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging, set_logging_level

from button import button
from oled import OLED

async def main(args: argparse.Namespace):
    oled = OLED()
    oled.write(["Starting"])
    setup_logging(__name__, args.log, {'bleak':logging.INFO})
    set_logging_level(logging.INFO)

    async with WirelessGoPro(
            args.identifier,
            enable_wifi=False,
            interfaces={WirelessGoPro.Interface.BLE},
            host_sudo_password='raspberry'
    ) as gopro:
        oled.write(["Connecting", "to WiFi"])
        await gopro.access_point.connect(args.ssid, args.password)

        # Now wait for at button press to start streaming
        while True:
            oled.write(["Waiting","for button"])
            await button()

            oled.write(["Streaming", "Now"])
            await gopro.streaming.start_stream(
                streaming.StreamType.LIVE,
                streaming.LivestreamOptions(
                    url=args.url,
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
    parser.add_argument("ssid", type=str, help="WiFi SSID to connect to.")
    parser.add_argument("password", type=str, help="Password of WiFi SSID.")
    parser.add_argument("url", type=str, help="RTMP server URL to stream to.")
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
    return add_cli_args_and_parse(parser, wifi=False)


if __name__ == "__main__":
    try:
        asyncio.run(main(parse_arguments()))
    except Exception as e:
        print(e)

