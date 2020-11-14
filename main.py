import os
import sys
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


def parse_cmd():
    mission_list = {}
    params = sys.argv

    if len(params) != 10:
        print("7 Missions must be provided ", len(params) - 1, " were provided")
        exit()

    instance = str(params[1])
    instance_to_kill = str(params[2])

    print("The following Missions will be launched:")
    for i in range(3, 10):
        mission_list[i - 3] = params[i]
        print("Weekday:", i - 3, "Mission:", str(params[i]))

    return mission_list, instance, instance_to_kill


launch_timeout = 10  # In Seconds
launch_prefix = "--net"
launch_params = ""
refresh_rate = 60  # In Seconds

mission_list, instance, instance_to_kill = parse_cmd()

while True:
    weekday = datetime.datetime.today().weekday()
    print("Launching Mission for Weekday #", weekday)
    launch_process(instance, launch_params, launch_prefix, mission_list[weekday], launch_timeout)
    block_if_running(instance_to_kill, weekday, refresh_rate)
