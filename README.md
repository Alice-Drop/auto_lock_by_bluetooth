# Automatic Computer Locking Based on Bluetooth Device Disconnection

[简体中文](https://github.com/Alice-Drop/auto_lock_by_bluetooth/blob/main/README-zh.md) | English

Do you often forget to lock your computer before walking away, only to worry that someone might access it?

A common solution is to buy a camera that supports Windows Hello and uses its automatic locking feature when you leave. However, this can be quite expensive.

This software is designed to use your regular Bluetooth devices to help lock your computer, so you can have the automatic locking feature without spending any extra money.

For instance, when I leave my computer, I usually take my Bluetooth headphones with me. As I walk away, the connection is lost. Or, after finishing some work, I might put my headphones on the desk but forget to lock the computer before leaving.

We can observe that, as long as my headphones are no longer connected to my computer, it's very likely that I’m no longer using it.

This software is based on that principle to protect your computer.

Not just headphones, you can set any Bluetooth device that can be detected by your computer as a protector, such as your phone, Bluetooth tags, etc.

Additionally, if your headphones are not connected when unlocking your computer, the program will automatically pause the lock detection to avoid misinterpreting your intentions in situations where you’re not wearing headphones. Once you reconnect the headphones, automatic locking will resume.

### How to Use?

Download the release, unzip the folder, and run `launcher.py`. Set your Bluetooth device name and click "Start Detection."

The .exe version will be available soon.