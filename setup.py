import os

from cx_Freeze import setup, Executable

APPLICATION_NAME = "Assembly PDF Generator"
APPLICATION_VERSION = "1.0.0"

os.environ['TCL_LIBRARY'] = r'{}\tcl\tcl8.6'.format(os.environ["PYTHON36_HOME"])
os.environ['TK_LIBRARY'] = r'{}\tcl\tk8.6'.format(os.environ["PYTHON36_HOME"])

includefiles = [os.path.join(os.environ["PYTHON36_HOME"], 'DLLs', 'tk86t.dll'),
                os.path.join(os.environ["PYTHON36_HOME"], 'DLLs', 'tcl86t.dll')]
includes = []
excludes = []
packages = ['asyncio']

setup(
    name=APPLICATION_NAME,
    version=APPLICATION_VERSION.replace("-SNAPSHOT", ""),
    options={'build_exe': {'excludes': excludes,
                           'packages': packages,
                           'include_files': includefiles}},
    executables=[Executable("main.py", targetName="{}.exe".format(APPLICATION_NAME), base="Win32GUI")])
