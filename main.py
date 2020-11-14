import os
import time
import psutil
import datetime

def kill_process(name):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == name:
            proc.kill()


def process_running(name):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == name:
            return True
    return False


def make_string(instance, launch_params, launch_prefix, mission):
    build = instance + " " + launch_params + " " + launch_prefix + " " + mission
    print(build)
    return build


def launch_process(instance, launch_params, launch_prefix, mission, launch_timeout):
    os.system(make_string(instance, launch_params, launch_prefix, mission))
    time.sleep(launch_timeout)


def in_current_time_slice(weekday, test):
    print(datetime.datetime.today().weekday())
    if datetime.datetime.today().weekday() == weekday:
        return True
    return False


def block_if_running(instance_to_kill, weekday, refresh_rate):
    test = False
    while process_running(instance_to_kill) and in_current_time_slice(weekday, test):
        time.sleep(refresh_rate)
    if process_running(instance_to_kill):
        kill_process(instance_to_kill)
        print("Process Killed")
    else:
        print("Process Died")


instance = "E:/SteamLibrary/steamapps/common/DCSWorld/bin/DCS.exe"  # Replace with your Path
launch_timeout = 5  # In Seconds
launch_prefix = "--net"
launch_params = "--force_disable_VR"
instance_to_kill = "DCS.exe"
refresh_rate = 1  # In Seconds

mission_list = {
    1: "E:/SteamLibrary/steamapps/common/Mission/Operation_Clear_Field_v123_5.miz",  # Monday
    2: "E:/SteamLibrary/steamapps/common/Mission/Georgian_Power_v080.miz",  # Tuesday
    3: "E:/SteamLibrary/steamapps/common/Mission/Persian_Power_v080.miz",  # Wednesday
    4: "E:/SteamLibrary/steamapps/common/Mission/Syrian_Power_v080.miz",  # Thursday
    5: "E:/SteamLibrary/steamapps/common/Mission/Operation_Clear_Field_v123_5.miz",  # Friday
    6: "E:/SteamLibrary/steamapps/common/Mission/Operation_Clear_Field_v123_5.miz",  # Saturday
    7: "E:/SteamLibrary/steamapps/common/Mission/Operation_Clear_Field_v123_5.miz",  # Sunday
}

while True:
    weekday = datetime.datetime.today().weekday()
    print("Launching Mission for Weekday #", weekday)
    launch_process(instance, launch_params, launch_prefix, mission_list[weekday], launch_timeout)
    block_if_running(instance_to_kill, weekday, refresh_rate)
