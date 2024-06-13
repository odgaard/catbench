# setup.py
from setuptools import setup, find_packages

setup(
    name='catbench',
    version='0.1.0',
    packages=find_packages(),
    license='LICENSE',
    description='A benchmarking framework for autotuning',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    # Include requirements from requirements.txt
    install_requires=open('requirements.txt', encoding='utf-8').read().splitlines(),
)
