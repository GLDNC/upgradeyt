from cx_Freeze import setup, Executable

# Define o build_exe_options para criar um único arquivo executável
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

setup(
    name = "YourAppName",
    version = "0.1",
    description = "Your Application Description",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base="Win32GUI")]  
)