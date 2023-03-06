import requests
import subprocess
import sys
from tqdm import tqdm

current_version = "0.0.1"
repo_name = "updateAppTest"
github_username = "cltWilly"

# Get the latest release information from the GitHub API
url = f"https://api.github.com/repos/{github_username}/{repo_name}/releases/latest"
response = requests.get(url)
if response.ok:
    data = response.json()
    latest_version = data["tag_name"]
    for asset in data["assets"]:
        if asset["name"].endswith(".exe"):
            download_url = asset["browser_download_url"]
            break
else:
    print(f"Failed to get release information for {github_username}/{repo_name}")
    sys.exit()

# Check if the current version is up to date
if latest_version == current_version:
    print(f"App is up to date! {current_version}")
else:
    print(f"App is not up to date! App is on version {current_version} but could be on version {latest_version}!")
    print("Downloading new version now!")
    response = requests.get(download_url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open("temp_main.exe", "wb") as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    with open("update.bat", "w") as f:
        f.write(f'@echo off\n'
                f'taskkill /f /im main.exe\n'
                f'del main.exe\n'
                f'ren temp_main.exe main.exe\n'
                f'start main.exe\n'
                f'del "%~f0"')
    subprocess.Popen(["update.bat"])
    sys.exit()
