from setuptools import setup, find_packages

setup(
    name="agent_05_migration_tests",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytest>=8.4.0",
        "pytest-asyncio>=0.23.5",
        "pytest-cov>=4.1.0",
        "pytest-xdist>=3.5.0",
        "pytest-timeout>=2.2.0"
    ]
)
