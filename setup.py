from setuptools import setup

setup(name='treeconvert',
      version='1.0',
      python_requires='>=3.7',
      description='Convert NML files to SWC files',
      url='https://github.com/ariadne-service/treeconvert',
      author='ariadne-service gmbh',
      author_email='contact@ariadne.ai',
      license='zlib',
      packages=['treeconvert'],
      entry_points={
          'console_scripts': [
              'treeconvert = treeconvert.__main__'
          ]
      },
      install_requires=['declxml'])
