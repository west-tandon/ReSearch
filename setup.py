from setuptools import setup, Extension

research_c_utils = Extension('research_c_utils', sources=['research/research_c_utils.c'])

setup(name='ReSearch',
      version='1.0',
      description='Research tools for Text Search and Information Retrieval',
      download_url='https://github.com/west-tandon/ReSearch',
      license='MIT',
      packages=['research', 'research.coding', 'research.index'],
      ext_modules=[research_c_utils],
      install_requires=[
          'argparse',
          'importlib'
      ])
