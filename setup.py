from setuptools import setup, find_packages

setup(
    name="ftp_brute_force_tool",
    version="0.1.0",
    author="Jackson Ja",
    author_email="jackson2937703346@163.com",
    description="A FTP brute force tool",
    long_description=open("README_en.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jacksonjapy/ftp_brute_force",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[],
)
