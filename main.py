import time
import os
import pyautogui
import asyncio
from bleak import BleakScanner
import json

async def is_device_connected(target_name):
    """检查是否有指定名称的蓝牙设备连接"""
    try:
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"比较中：{device.name}")
            if target_name.lower() in device.name.lower():
                
                return True
        return False
    except Exception as e:
        if f"{e}" == "'NoneType' object has no attribute 'lower'":
            print("未连接耳机")
        else:
            print(f"蓝牙检测错误: {e}")
        return False

def lock_computer():
    """锁定计算机"""
    try:
        os.system('rundll32.exe user32.dll,LockWorkStation')  # Windows下锁定计算机
        print("电脑已锁定")
    except Exception as e:
        print(f"锁定电脑时出错: {e}")

def is_computer_locked():
    """判断计算机是否被锁定，通过检查当前活动用户"""
    try:
        current_user = os.getlogin()
        return False  # 如果能获取当前用户，说明电脑未锁定
    except OSError:
        return True  # 如果无法获取当前用户，说明电脑被锁定


if __name__ == "__main__":

    DEFAULT_CONFIG = {
        "Bluetooth_Device_Name": "EarFun Air Pro 4",
        "Detection_Gap": 30
    }
    CONFIG_PATH = "./config.txt"

    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as myFile:
            config = json.load(myFile)
            BLUETOOTH_DEVICE_NAME = config["Bluetooth_Device_Name"]
            DETECTION_GAP = config["Detection_Gap"]
    else:
        with open(CONFIG_PATH, "w", encoding="utf-8") as myFile:
            json.dump(DEFAULT_CONFIG, myFile)
            BLUETOOTH_DEVICE_NAME = DEFAULT_CONFIG["Bluetooth_Device_Name"]
            DETECTION_GAP = DEFAULT_CONFIG["Detection_Gap"]

    target_device_name = BLUETOOTH_DEVICE_NAME  # 蓝牙耳机名称
    was_locked = False
    enable = False  # 一开始不确定有没有耳机，先这样，等第一次检测

    while True:
        if asyncio.run(is_device_connected(target_device_name)):
            print("耳机已连接，继续检测...")
            was_locked = False  # 如果连接上耳机，重置锁定标志
            enable = True  # 启用锁定
        else:
            if (not was_locked) and enable:
                print("耳机未连接，锁定电脑...")
                lock_computer()
                was_locked = True

            # 等待用户解锁计算机
            while was_locked:
                print("检测到电脑锁定，等待解锁...")
                time.sleep(10)
                if not is_computer_locked():  # 如果电脑解锁
                    print("电脑已解锁，恢复检测...")
                    was_locked = False
                    if not asyncio.run(is_device_connected(target_device_name)):
                        print("解锁后未检测到耳机，自动disable锁定功能")
                        enable = False

        time.sleep(DETECTION_GAP)  # 每隔30秒检测一次
