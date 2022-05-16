from setuptools import find_packages, setup

setup(
    name='text_processing',
    packages=find_packages(),
    version='0.1.0',
    description='Text utils used by Plataforma Telar',
    author='@indonoso',
    install_requires=['tqdm', 'textract', 'spacy', 'emoji']
)
