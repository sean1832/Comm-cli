import json
import os
import platform
import shutil
from pathlib import Path
import traceback


def get_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_version():
    with open(Path(get_root(), "nx/manifest.json")) as f:
        data = json.load(f)
        return data["version"]


def move_to_dir(source, target):
    os.makedirs(target, exist_ok=True)
    shutil.move(source, target)


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


def zip_dir(target_dir, root_dir, name):
    shutil.make_archive(target_dir, "zip", root_dir=root_dir, base_dir=name)


if __name__ == "__main__":
    os_name = check_os()

    dist_root = Path(get_root(), "dist").resolve()
    version = get_version()

    if os_name == "macOS":
        try:
            source_exe = Path(dist_root, "NetXchanger.app").resolve().as_posix()

            target_exe = (
                Path(dist_root, f"NetXchanger_v{version}_mac/NetXchanger.app")
                .resolve()
                .as_posix()
            )

            move_to_dir(source_exe, target_exe)

            shutil.make_archive(
                target_exe,
                "zip",
                dist_root,
                f"NetXchanger_v{version}_mac",
            )
        except Exception as e:
            print(e)
            traceback.print_exc()
            exit(1)

    elif os_name == "Windows":
        source_root = Path(dist_root, "NetXchanger").resolve()
        if not source_root.exists():
            exit(f"{source_root}, directory does not exist.")

        target_root = Path(dist_root, f"NetXchanger_v{version}_win").resolve()

        # remove old directory
        if target_root.exists():
            shutil.rmtree(target_root)

        os.rename(source_root, target_root)

        shutil.make_archive(
            str(target_root),
            "zip",
            dist_root,
            f"NetXchanger_v{version}_win",
        )
        print(f"Done. {target_root}.zip is created.")
    elif os_name == "Linux":
        raise NotImplementedError("Linux is not supported yet.")

    else:
        raise OSError("Unknown OS.")
