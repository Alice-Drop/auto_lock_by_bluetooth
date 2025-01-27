import time
import os
import pyautogui
import asyncio
from bleak import BleakScanner
import json
from typing import List

DEFAULT_CONFIG = {
    "Bluetooth_Device_Name": "EarFun Air Pro 4",
    "Detection_Gap": 30
}
CONFIG_PATH = "./config.txt"


async def scan_available() -> List[str]:
    # 获取所有当前连接的蓝牙设备
    try:
        devices = await BleakScanner.discover()
        return [item.name for item in devices if item.name]
    except Exception as e:
        print(f"蓝牙检测错误: {e}")  # todo: 未来加上GUI后，在这里raise，然后在主程序catch
        return []


def ask_for_setting_termux():
    # 暂时用终端来实现
    print("欢迎使用！请稍等，正在扫描设备....")
    my_devices = asyncio.run(scan_available())
    print(my_devices)
    print("\n扫描结果如下：")
    for i in range(len(my_devices)):
        print(f"{i}. {my_devices[i]}")

    selected_device_name = ""
    while not selected_device_name:
        device_choice = input("\n你希望用哪个作为判断是否离开的设备？（请输入序号）")
        try:
            selected_device_name = my_devices[int(device_choice)]
        except ValueError or IndexError:
            print("输入的序号无效！请重新输入。")
    print("选择了", selected_device_name)

    gap_choice = input("\n默认每隔30秒检查一次设备是否连接。这个间隔越小越安全，但对性能要求更高。\n"
                       "如果需要更改，请输入你希望的秒数；如果不需要，请直接按下回车。")
    if gap_choice:
        selected_gap = int(gap_choice)
    else:
        selected_gap = 30

    config = {
        "Bluetooth_Device_Name": selected_device_name,
        "Detection_Gap": selected_gap
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as my_file:
        json.dump(config, my_file)


if __name__ == "__main__":
    """
    这个的作用只是检查是否设置好，没设置好不许进。未来可能作为一个控制器放在托盘。
    流程：
    看是否有设置用哪个设备（找数据文件，看看
    如果没有，那就检测所有已连接的蓝牙设备，问要用那个。设置完之后，
    
    如果有了设置，那就开启。
    
    """

    while not os.path.exists(CONFIG_PATH):
        ask_for_setting_termux()

    os.system("start /MIN main.py")
