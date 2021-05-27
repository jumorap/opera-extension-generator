import json
import requests
import shutil
from PIL import Image


print("\n ___       ____  _    _____           __    ____  _"
      "\n/ / \     | |_  \ \_/  | |   __      / /`_ | |_  | |\ |  __"
      "\n\_\_/     |_|__ /_/ \  |_|  (_()     \_\_/ |_|__ |_| \| (_()")

print("By: Jumorap\n")

extension_name = str(input("Extension name: "))
sidebar_name = str(input("Sidebar name: "))
functions_description = str(input("Describe the functionalities: "))
sidebar_description = str(input("Describe the extension: "))
url_of_page = str(input("Url of website to render: "))

url_logo = str(input("Url of logo image (png): "))

extension_version = str(input("Version (1.0): "))

# Images default sizes
default_sizes = [19, 38, 48, 128]

# Name of image basic file to upload
image_result = 'upload_this/logos/logo.png'

# Is generated the json structure with the user values to be verified by Opera addons
messages_to_json = {
    "extName": {
        "description": extension_name,
        "message": sidebar_name
    },
    "extDescription": {
        "description": functions_description,
        "message": sidebar_description
    },
    "extPanelURL": {
        "description": url_of_page,
        "message": url_of_page
    }
}


# Updating the value version in manifest.json. The default value is 1.0
# And Updating eh message value to Opera addons
def updating_json_files(ext_ver, mess_json):
    print("\n...Generating resources\n")

    if ext_ver == "":
        ext_ver = 1.0

    read_json = json.loads(open('upload_this/manifest.json').read())
    read_json["version"] = ext_ver

    with open('upload_this/manifest.json', 'w') as json_update:
        json.dump(read_json, json_update)

    with open('upload_this/_locales/en/messages.json', 'w') as json_file:
        json.dump(mess_json, json_file)


# Is downloaded the user image and saved as 'logo.png' in 'upload_this/logos'
def download_load_image(url, name):
    print("...Getting logo\n")
    try:
        r = requests.get(url, stream=True)

        with open(name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        return False

    except:
        print("ERROR: Not possible to get the logo. Try again with another URL logo in format .png")

        return True


# Is resized by default sizes the image uploaded by user
def resize_logos(logo_route, sizes, error):
    if not error:
        print("...Resizing logo\n")

        for size in sizes:
            resizing = Image.open(logo_route).resize((size, size))
            resizing.save(f'upload_this/logos/logo{size}x{size}.png')

        return True

    return False


updating_json_files(extension_version, messages_to_json)
get_error = download_load_image(url_logo, image_result)
no_error = resize_logos(image_result, default_sizes, get_error)

print("Complete."
      "\nNow, go to opera://extensions in your Opera browser, "
      "\nTurn on the developer mode option "
      "\nClick in Load unpacked"
      "\nGo to the file '/opera-extension-generator' and select the folder '/upload_this'"
      "\nEnjoy of your Opera sidebar extension") if no_error else print("State: ERROR")
