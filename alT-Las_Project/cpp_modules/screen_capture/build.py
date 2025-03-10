# -*- coding: utf-8 -*-
import subprocess
import platform
import os

def compile_cpp_module():
    """
    C++ modülünü derler.
    """
    source_file = "screen_capture.cpp"
    if platform.system() == "Windows":
        output_file = "screen_capture.dll"
        compile_command = [
            "g++",
            "-shared",
            "-o", output_file,
            source_file,
            "-I", ".",
            "-l", "gdiplus"
        ]
    elif platform.system() == "Linux":
        output_file = "screen_capture.so"
        compile_command = [
            "g++",
            "-shared",
            "-fPIC",
            "-o", output_file,
            source_file,
            "-I", ".",
            "-l", "Imlib2"
        ]
    elif platform.system() == "Darwin":
        output_file = "screen_capture.dylib"
        compile_command = [
            "g++",
            "-shared",
            "-o", output_file,
            source_file,
            "-I", ".",
            "-l", "Imlib2"
        ]
    else:
        print("İşletim sistemi desteklenmiyor.")
        return

    try:
        subprocess.run(compile_command, check=True)
        print(f"Derleme başarılı: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Derleme hatası: {e}")

if __name__ == "__main__":
    compile_cpp_module()
