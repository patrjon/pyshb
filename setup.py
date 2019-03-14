import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyshb",
    version="0.0.1",
    author="Patrick Jonsson",
    author_email="patrickjonssonbbg@gmail.com",
    description="PySHB is a Python package to parse transaction files downloaded from www.handelsbanken.se "
                "(Svenska Handelsbanken AB).",
    long_description=long_description,
    long_description_content_type="markdown",
    url="https://github.com/patrjon/pyshb.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
