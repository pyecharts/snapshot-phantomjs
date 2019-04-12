import io
import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] == 2

PHANTOMJS_EXEC = "phantomjs"
DEFAULT_OUTPUT_NAME = "output.%s"
NOT_SUPPORTED_FILE_TYPE = "Not supported file type '%s'"

MESSAGE_GENERATING = "Generating file ..."
MESSAGE_PHANTOMJS_VERSION = "phantomjs version: %s"
MESSAGE_FILE_SAVED_AS = "File saved in %s"
MESSAGE_NO_SNAPSHOT = (
    "No snapshot taken by phantomjs. "
    "Please make sure it is installed and available on your PATH!"
)
MESSAGE_NO_PHANTOMJS = "No phantomjs found in your PATH. Please install it!"


def make_snapshot(
    html_path: str, file_type: str, pixel_ratio: int = 2, delay: int = 2, **_
):
    chk_phantomjs()
    logger.info(MESSAGE_GENERATING)
    __actual_delay_in_ms = int(delay * 1000)
    # add shell=True and it works on Windows now.
    proc_params = [
        PHANTOMJS_EXEC,
        os.path.join(get_resource_dir("phantomjs"), "snapshot.js"),
        to_file_uri(html_path),
        file_type,
        str(__actual_delay_in_ms),
        str(pixel_ratio),
    ]
    proc = subprocess.Popen(
        proc_params,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=get_shell_flag(),
    )
    if PY2:
        content = proc.stdout.read()
        content = content.decode("utf-8")
    else:
        content = io.TextIOWrapper(proc.stdout, encoding="utf-8").read()

    return content


def get_resource_dir(folder):
    current_path = os.path.dirname(__file__)
    resource_path = os.path.join(current_path, folder)
    return resource_path


def chk_phantomjs():
    try:
        phantomjs_version = subprocess.check_output(
            [PHANTOMJS_EXEC, "--version"], shell=get_shell_flag()
        )
        phantomjs_version = phantomjs_version.decode("utf-8")
        logger.info(MESSAGE_PHANTOMJS_VERSION % phantomjs_version)
    except Exception:
        logger.warn(MESSAGE_NO_PHANTOMJS)
        sys.exit(1)


def get_shell_flag():
    return sys.platform == "win32"


def to_file_uri(a_file_name):
    __universal_file_name = a_file_name.replace("\\", "/")
    if ":" not in a_file_name:
        __universal_file_name = os.path.abspath(__universal_file_name)
    return "file:///{0}".format(__universal_file_name)
