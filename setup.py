import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='python-e3dc',
    version='0.0.1',
    packages=['python_e3dc'],
    url='https://www.github.com/python-e3dc',
    license='MIT',
    author='J. Brunswicker',
    author_email='johannes.brunswicker@gmail.com',
    description='',
    long_description=read('README.md'),
    install_requires=['py3rijndael', 'libscrc'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries"
    ]
)
