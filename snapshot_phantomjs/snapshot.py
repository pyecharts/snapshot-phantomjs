import io
import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)

PHANTOMJS_EXEC = "phantomjs"


def make_snapshot(
    html_path: str, file_type: str, delay: int = 2, pixel_ratio: int = 2, **_
):
    chk_phantomjs()
    logger.info("Generating file ...")
    proc_params = [
        PHANTOMJS_EXEC,
        os.path.join(get_resource_dir("phantomjs"), "snapshot.js"),
        to_file_uri(html_path),
        file_type,
        str(int(delay * 1000)),
        str(pixel_ratio),
    ]
    proc = subprocess.Popen(
        proc_params,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        # shell=True will make Windows happy.
        shell=get_shell_flag(),
    )
    content = io.TextIOWrapper(proc.stdout, encoding="utf-8").read()
    return content


def get_resource_dir(folder: str) -> str:
    current_path = os.path.dirname(__file__)
    resource_path = os.path.join(current_path, folder)
    return resource_path


def chk_phantomjs():
    try:
        phantomjs_version = subprocess.check_output(
            [PHANTOMJS_EXEC, "--version"], shell=get_shell_flag()
        )
        phantomjs_version = phantomjs_version.decode("utf-8")
        logger.info("phantomjs version: %s" % phantomjs_version)
    except Exception:
        logger.warning("No phantomjs found in your PATH. Please install it!")
        sys.exit(1)


def get_shell_flag() -> bool:
    return sys.platform == "win32"


def to_file_uri(file_name: str) -> str:
    __universal_file_name = file_name.replace("\\", "/")
    if ":" not in file_name:
        __universal_file_name = os.path.abspath(__universal_file_name)
    return "file:///{0}".format(__universal_file_name)
