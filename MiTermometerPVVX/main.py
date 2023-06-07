import asyncio
import datetime
import os

# import struct
from bleak import BleakScanner

# MiTermometerPVVX


async def main():
    ATC_SERVICE = "0000181a-0000-1000-8000-00805f9b34fb"
    stop_event = asyncio.Event()
    atc_counters = {}
    atc_date = {}
    # atc_devices = {"00:00:00:00:99:5B": "ATC-1-995B", "00:00:00:00:DB:77": "ATC-2-DB77"}
    atc_devices = {}
    atc_devices_order = []

    print_pos = {"x": 0, "y": 0}

    def print_text_pos(x, y):
        print_pos["x"] = x
        print_pos["y"] = y

    def print_text(text):
        print("\033[" + str(print_pos["y"]) + ";" + str(print_pos["x"]) + "H" + text)
        print_pos["y"] += 1

    def print_clear():
        os.system("cls")

    def callback(device, advertising_data):
        adv_atc = advertising_data.service_data.get(ATC_SERVICE)
        if not adv_atc:
            return

        # if device.address not in atc_devices:
        #     return
        # print("device:\t", device)
        # print(f"advertising_data:\t  {advertising_data}")
        if advertising_data:
            name = advertising_data.local_name

            if device.address not in atc_devices:
                if len(atc_devices) == 0:
                    print_clear()
                atc_devices[device.address] = {"name": name, "id": len(atc_devices)}

            if not name:
                name = atc_devices.get(device.address)["name"]
                if not name:
                    name = "ATC-" + "".join(device.address.split(":")[-2:])
                    atc_devices[device.address]["name"] = name
        # print(atc_devices)
        # if name and name[0:3] == "ATC":
        if True:
            rssi = advertising_data.rssi
            # adv_atc = advertising_data.service_data[ATC_SERVICE]
            if adv_atc:
                count = int.from_bytes(adv_atc[13:14], byteorder="little", signed=False)
                # (temp,humidity,battery_v,battery,count) = struct.unpack('<hhHBB',adv_atc[6:14])
                if atc_counters.get(device.address) != count:
                    atc_counters.update({device.address: count})
                    date_now = datetime.datetime.now()
                    date_prev = atc_date.get(device.address)
                    if date_prev:
                        date_diff = date_now - date_prev
                        date_diff = datetime.timedelta(
                            seconds=round(date_diff.total_seconds())
                        )
                    else:
                        date_diff = 0
                    atc_date.update({device.address: date_now})
                    temp = int.from_bytes(adv_atc[6:8], byteorder="little", signed=True)
                    humidity = int.from_bytes(
                        adv_atc[8:10], byteorder="little", signed=True
                    )
                    battery_v = int.from_bytes(
                        adv_atc[10:12], byteorder="little", signed=False
                    )
                    battery = int.from_bytes(
                        adv_atc[12:13], byteorder="little", signed=False
                    )
                    # flag=int.from_bytes(adv_atc[14:15], byteorder='little', signed=False)
                    temp = temp / 100.0
                    humidity = humidity / 100.0
                    battery_v = battery_v / 1000.0

                    # print(atc_devices[device.address])
                    id = atc_devices[device.address]["id"]
                    h1 = 12
                    h2 = 8
                    gap = 15
                    name_len = h1 + h2
                    text_width = name_len + gap
                    text_hight = 10 + 3
                    cols = 4
                    posx = text_width * (id % cols)
                    posy = text_hight * (id // cols) + 1
                    print_text_pos(posx, posy)
                    # print_text(f"{'device:':<{h1}}{name}")
                    print_text("{:<12}{:<8}".format("device:", name))
                    print_text("-" * name_len)
                    print_text("{:<12}{:<8}".format("temp:", f"{temp:.2f} \xB0C"))
                    print_text("{:<12}{:<8}".format("humidity:", f"{humidity:.2f} %"))
                    print_text("{:<12}{:<8}".format("batteryv:", f"{battery_v} V"))
                    print_text("{:<12}{:<8}".format("battery:", f"{battery} %"))
                    print_text("{:<11}{:<8}".format("rssi:", f"{rssi} dB"))
                    print_text("{:<12}{:<8}".format("count:", f"{count}"))
                    print_text(
                        "{:<12}{:<8}".format(
                            "time now:", f"{date_now.strftime('%H:%M:%S')}"
                        )
                    )
                    if date_diff:
                        print_text(
                            "{:<12}{:<8}".format("Duration:", f"{str(date_diff)}")
                        )

    try:
        mode = "passive"
        # mode = "active"
        print_clear()
        print(
            f"Scanning BLE devices of type 'ATC_MiThermometer (PVVX)' in {mode} mode, please wait..."
        )

        async with BleakScanner(callback, scanning_mode=mode):
            await stop_event.wait()

    except asyncio.CancelledError:
        print("**** task scanner cancelled")
        stop_event.set()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(str(e))
