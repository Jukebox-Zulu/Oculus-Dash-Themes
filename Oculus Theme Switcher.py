import shutil
import os
import time
import json

options = {
    1: 'grid_plane_003.dds',
    2: 'grid_plane_004.dds',
    3: 'grid_plane_007.dds',
    4: 'default.dds',
    5: False
}

options_legible = {
    1: "Gray with dots.",
    2: "Black with dots.",
    3: "Black with grid.",
    4: "Default white with grid."
}

with open('settings.json', 'r') as f:
    settings = json.load(f)

path = settings.get("path")
if not path:
    path_inp = input(
        'Please copy and paste the path to your Oculus dashboard texture folder.\nThe default path is "C:\\Oculus\\Support\\oculus-dash\\dash\\assets\\raw\\textures\\environment\\the_void"\n\n')
    settings["path"] = path_inp.replace('\\', '\\')
    path = settings.get("path")
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=2)


current = options.get(settings.get("current_setting"))
files = os.listdir(path)
wd = os.getcwd()
print('Your current setting is ' + options_legible.get(settings.get("current_setting")) + '\n')

if "default.dds" not in files and settings.get('backup') and settings.get("current_setting") != 4:
    updated = True
    settings["backup"] = False
    print("WARNING: Client update detected. If you would like to retain your current setting, choose option 5.\n")
else:
    updated = False

option = int(input('Choose a dashboard option then hit enter: \n1. Gray with dots\n2. Black with dots\n3. Black with grid\n4. Original white grid\n5. Keep or restore current setting.\n').strip('.'))

choice = options.get(option)


if not choice:
    if not updated:
        print('\nClosing automatically in three seconds.')
        time.sleep(3)
        exit()
    choice = current
    option = settings.get("current_setting")
old = os.path.join(path, current)
new = os.path.join(path, choice)
working = os.path.join(path, 'grid_plane_006.dds')
default = os.path.join(path, 'default.dds')
if old == new and not updated:
    print('You are already using this theme.')
    time.sleep(3)
    exit()

try:
    if not settings.get("backup"):
        if updated:
            print('Client update detected, creating new backups...')
            for file in os.listdir(os.path.join(wd, 'Oculus Dash Backups')):
                os.remove(os.path.join(wd, 'Oculus Dash Backups', file))
        else:
            print('Creating backup on first run...')
            try:
                os.remove(os.path.join(wd, 'Oculus Dash Backups', 'null.txt'))
            except FileNotFoundError:
                pass
        for file in files:
            shutil.copy(os.path.join(path, file), os.path.join(wd, 'Oculus Dash Backups', file))
        settings["backup"] = True
        print('Backup created successfully.')
    backups = os.listdir(os.path.join(wd, 'Oculus Dash Backups'))
    for file in files:
        os.remove(os.path.join(path, file))
    for file in backups:
        shutil.copy(os.path.join(wd, 'Oculus Dash Backups', file), os.path.join(path, file))
    if option != 4:
        shutil.copy(working, default)
        shutil.move(new, working)

except PermissionError:
    print('Encountered a permission error, please run this program in administrator mode.')
    time.sleep(5)
    exit()
except FileNotFoundError:
    print('One or more files were not found. The program may need to be updated, or you may want to restore manually from the backup folder.')
    time.sleep(5)
    exit()
settings['current_setting'] = option
with open('settings.json', 'w') as f:
    json.dump(settings, f, indent=2)
print('Theme changed successfully. Remember to restart your Oculus Client.\nClosing automatically in five seconds.')
time.sleep(5)
exit()
