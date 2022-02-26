from ensurepip import version
from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name='PathFinding-Simulator',
    version='0.0.1',
    description="Simulator Path-Finding Algorithms written in Python",
    # long_description=readme,
    author="Toan (Nico) Le",
    author_email="leductoan1210@gmail.com",
    url="",
    license=license,
    packages=find_packages(exclude={'tests', 'docs'}),
)