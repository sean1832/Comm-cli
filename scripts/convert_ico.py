import os
import platform
import shutil
import subprocess
from pathlib import Path

from PIL import Image


def convert_ico(png_path, ico_path, sizes=(16, 32, 48, 64, 128, 256)):
    """
    Convert a PNG image to an ICO file with multiple resolutions.

    png_path: Path to the source PNG file.
    ico_path: Path to save the ICO file.
    sizes: Tuple of sizes (in pixels) for the ICO file.

    >>> convert_ico("icon.png", "icon.ico")
    """
    with Image.open(png_path) as img:
        # Create a list to hold the resized images
        ico_images = []

        for size in sizes:
            # Resize the image and append to the list
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            ico_images.append(resized_img)

        # Save all resized images as a single ICO file
        ico_images[0].save(
            ico_path, format="ICO", sizes=[(size, size) for size in sizes]
        )


def convert_icns(png_path, icns_path, temp_folder, sizes=(16, 32, 48, 64, 128, 256)):
    """
    Prepare images and convert them to an ICNS file.

    png_path: Path to the source PNG file.
    output_icns_path: Path to save the ICNS file.
    temp_folder: Folder to save resized images.
    sizes: Tuple of sizes (in pixels) for the ICNS file.

    >>> convert_icns("icon.png", "icon.icns", "temp")
    """

    iconset_folder = os.path.join(temp_folder, "icon.iconset")
    os.makedirs(iconset_folder, exist_ok=True)

    # Create resized images
    with Image.open(png_path) as img:
        for size in sizes:
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            resized_img.save(os.path.join(iconset_folder, f"icon_{size}x{size}.png"))

    # Convert to ICNS
    subprocess.run(["iconutil", "-c", "icns", iconset_folder, "-o", icns_path])

    # Delete temporary folder
    shutil.rmtree(iconset_folder)


def check_os():
    os_name = platform.system()

    if os_name == "Darwin":
        return "macOS"
    elif os_name == "Windows":
        return "Windows"
    elif os_name == "Linux":
        return "Linux"
    else:
        return "Unknown"


if __name__ == "__main__":
    # get project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    os_name = check_os()

    # check system
    if os_name == "macOS":
        print("Converting to ICNS...")
        source_img = Path(project_root, "nx/assets/icon.png").resolve().as_posix()
        target_img = Path(project_root, "nx/assets/icon.icns").resolve().as_posix()
        temp_folder = Path(project_root, "temp").resolve().as_posix()
        convert_icns(source_img, target_img, temp_folder)
    elif os_name == "Windows":
        print("Converting to ICO...")
        source_img = Path(project_root, "nx/assets/icon.png").resolve()
        target_img = Path(project_root, "nx/assets/icon.ico").resolve()
        temp_folder = Path(project_root, "temp").resolve()
        convert_icns(source_img, target_img, temp_folder)
    elif os_name == "Linux":
        raise NotImplementedError("Linux is not supported yet.")
    else:
        raise OSError("Unknown OS.")

    print("Done.")
