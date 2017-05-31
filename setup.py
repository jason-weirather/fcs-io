from setuptools import setup, find_packages
from codecs import open
from os import path

this_folder = path.abspath(path.dirname(__file__))
with open(path.join(this_folder,'README.md'),encoding='utf-8') as inf:
  long_description = inf.read()


setup(
  name='fcs-io',
  version='0.1.0',
  description='Class for reading and modifying FCS files',
  url='https://github.com/gusef/fcs-io',
  author='Jason L Weirather',
  author_email='jason.weirather@gmail.com',
  long_description=long_description,
  license='MIT License',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: MIT License'
  ],
  keywords='bioinformatics, flow cytometry, fcs, flow',
  packages=find_packages(),
  entry_points = {
    'console_scripts':['fcs-io=fcsio.cli:main']
  }
)

