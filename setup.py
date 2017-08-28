from distutils.core import setup

setup(
    name='EvoComp',
    version='0.1.0',
    author='JM Evangelista',
    packages=['EvoComp'],
    license='LICENSE.txt',
    description='Package for Evolutionary Computing',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy >= 1.13.1",
    ],
)