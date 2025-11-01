"""
Setup configuration for Azure DevOps Branch Manager
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="azure-devops-branch-manager",
    version="1.0.0",
    author="IranUdesha",
    author_email="",  # Add your email if you want
    description="A Python tool for locking and unlocking branches in Azure DevOps repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IranUdesha/azure-devops-branch-manager",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "azure-branch-manager=main:main",
        ],
    },
    keywords="azure devops git branch management lock unlock automation",
    project_urls={
        "Bug Reports": "https://github.com/IranUdesha/azure-devops-branch-manager/issues",
        "Source": "https://github.com/IranUdesha/azure-devops-branch-manager",
        "Documentation": "https://github.com/IranUdesha/azure-devops-branch-manager#readme",
    },
    include_package_data=True,
    zip_safe=False,
)