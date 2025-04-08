from setuptools import setup, find_packages

setup(
    name="human_design",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "pyswisseph>=2.10.0",
        "numpy>=1.20.0",
        "pytz>=2021.1",
        "python-dateutil>=2.8.2",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for Human Design calculations",
    keywords="human design, astrology, personality, body graph",
    url="https://github.com/yourusername/human_design",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
