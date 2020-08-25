import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="video2ascii",
    version="1.4.0",
    author="Iapetus-11",
    description="A package which goes through a video frame by frame and converts it into ascii art!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iapetus-11/video2ascii",
    packages=setuptools.find_packages(),
    install_requires=[
        'opencv-python'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
