from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="erp-system",
    version="1.0.0",
    author="ERP System Team",
    author_email="info@erpsystem.com",
    description="نظام إدارة المخزون المتكامل - Integrated ERP System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/DED",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
        "Natural Language :: Arabic",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "flake8>=6.1.0",
            "black>=23.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "erp-system=run:main",
        ],
    },
    include_package_data=True,
    package_data={
        "app": [
            "templates/**/*",
            "static/**/*",
        ],
    },
    zip_safe=False,
)

