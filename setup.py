import os
from setuptools import setup, find_packages


# currentdir = os.getcwd()

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

with open("LICENSE", "r", encoding="utf-8") as f:
    license_str = f.read()


setup(
    name="byesframe",
    version="0.1.0",
    author="Kaan Eraslan",
    python_requires=">=3.5.0",
    author_email="kaaneraslan@gmail.com",
    description="Trim video clips based on audio threshold",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license=license_str,
    packages=find_packages(
        exclude=[
            "tests",
            "*.tests",
            "*.tests.*",
            "tests.*",
            "docs",
            ".gitignore",
            "README.md",
        ]
    ),
    test_suite="tests",
    install_requires=[
        "moviepy",
        "pygame"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)
