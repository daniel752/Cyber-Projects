import ctypes
import subprocess
import sys
import os


def is_admin():
    try:
        admin = (os.getuid() == 0)  # if Unis
    except AttributeError:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0  # else if Windows
    return admin


def start_procmon():
    # Getting desktop path for all pc's (windows)
    desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
    cmd = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", "-File",
           desktop+r'\Procmon\start_procmon.ps1']  # Specify relative or absolute path to the
    # script
    subprocess.Popen(cmd, shell=True,)


if __name__ == "__main__":
    if is_admin():
        start_procmon()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
