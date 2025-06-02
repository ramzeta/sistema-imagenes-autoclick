from setuptools import setup, find_packages

setup(
    name="image_clicker_app",
    version="1.0.0",
    description="App de escritorio para detectar una imagen en pantalla y hacer clic automáticamente.",
    author="Rami",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "opencv-python",
        "pillow",
        "screeninfo"
    ],
    entry_points={
        "console_scripts": [
            "image-clicker=image_clicker.main:main"
        ]
    },
)
