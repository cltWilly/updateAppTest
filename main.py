import requests
import time

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
    quit()

# Check if the current version is up to date
if latest_version == current_version:
    print("App is up to date!")
else:
    print(f"App is not up to date! App is on version {current_version} but could be on version {latest_version}!")
    print("Downloading new version now!")
    new_version = requests.get(download_url)
    open("app.exe", "wb").write(new_version.content)
    print("New version downloaded, restarting in 5 seconds!")
    time.sleep(5)
    quit()
