import setuptools

import toascii

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="to-ascii",
    version=toascii.__version__,
    author="Iapetus-11",
    description=toascii.__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iapetus-11/To-ASCII",
    packages=setuptools.find_packages(),
    install_requires=["opencv-python"],
    data_files=[("", ["LICENSE"])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["asciify=toascii.cli:main"]},
)
