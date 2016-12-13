from distutils.core import setup, Extension

rsutils = Extension('rsutils', sources=['research/rsutils.c'])

setup (name='ReSearch',
       version='1.0',
       description='Research tools for Text Search and Information Retrieval',
       ext_modules=[rsutils])