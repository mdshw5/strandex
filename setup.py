from setuptools import setup

install_requires = ['six']

def get_version(string):
    """ Parse the version number variable __version__ from a script. """
    import re
    version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_str = re.search(version_re, string, re.M).group(1)
    return version_str

setup(
    name='strandex',
    version=get_version(open('strandex/__init__.py').read()),
    author='Matthew Shirley',
    author_email='mdshw5@gmail.com',
    url='https://github.com/mdshw5/strandex',
    description='Strand-anchored regex for expansion or contraction of FASTQ files',
    long_description=open('README.md').read(),
    packages=['strandex'],
    install_requires=install_requires,
    entry_points = { 'console_scripts': [ 'strandex = strandex:main' ] },
    license='MIT',
    classifiers=[
                "Development Status :: 3 - Alpha",
                "License :: OSI Approved :: MIT License",
                "Environment :: Console",
                "Intended Audience :: Science/Research",
                "Natural Language :: English",
                "Operating System :: Unix",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.5",
                "Topic :: Scientific/Engineering :: Bio-Informatics",
                ],
)
