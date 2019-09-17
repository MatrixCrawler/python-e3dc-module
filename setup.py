import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='e3dc',
    version='0.0.5',
    packages=setuptools.find_packages(),
    url='https://www.github.com/python-e3dc-module',
    license='MIT',
    author='J. Brunswicker',
    author_email='johannes.brunswicker@gmail.com',
    description='A Python library for querying E3/DC systems trough a RSCP connection.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['py3rijndael'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries"
    ]
)
