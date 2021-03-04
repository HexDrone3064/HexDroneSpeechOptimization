from setuptools import setup, find_packages
import os

readme_file = 'README.md'
readme = ''
if os.path.isfile(readme_file):
    with open(readme_file) as f:
        readme = f.read()

setup(
    name='hex-drone-optimized-speech-3064',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/HexDrone3064/HexDroneSpeechOptimization',
    license='MIT',
    author='⬡-Drone #3064',
    author_email='hexdrone3064@gmail.com',
    description='Speech optimization for ⬡-Drones. | Good Drones Obey HexCorp',
    long_description=readme
)
