import json
import requests
import shutil
from PIL import Image

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
    r = requests.get(url, stream=True)

    with open(name, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


# Is resized by default sizes the image uploaded by user
def resize_logos(logo_route, sizes):
    for size in sizes:
        resizing = Image.open(logo_route).resize((size, size))
        resizing.save(f'upload_this/logos/logo{size}x{size}.png')


updating_json_files(extension_version, messages_to_json)
download_load_image(url_logo, image_result)
resize_logos(image_result, default_sizes)
