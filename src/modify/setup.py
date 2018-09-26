import re
from setuptools import setup, find_packages

long_description = """
PDF modification package
"""

# Retrieve version number
VERSIONFILE = "pdf/convert/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))

setup(
    install_requires=[
        'PyPDF3>=1.0.1',
        'pdfrw',
        'PyMuPDF>=1.13.20',
        'Pillow',
        'reportlab',
        'PyBundle>=1.0.5',
        'PySimpleGUI>=3.6.2',
        'looptools',
        'tqdm',
    ],
    name='pdfconduit-modify',
    version=verstr,
    packages=find_packages(),
    namespace_packages=['pdf'],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfconduit',
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='PDF toolkit for preparing documents for distribution.',
    long_description=long_description,
)