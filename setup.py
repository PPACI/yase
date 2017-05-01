from distutils.core import setup

setup(
    name='yase',
    version='1.0.1',
    url='https://github.com/PPACI/yase',
    license='MIT',
    author='Pierre Paci',
    author_email='pierre.paci',
    description='Yet Another Sequence Encoder - Encode sequences to vector of vector in python !',
    install_requires=[
        'tqdm>=4.11.2',
        'numpy>=1.11.3'
    ],
    package_data={'yase': ['Ressources/*.json']},
    packages=['yase'],
    entry_points={
        'console_scripts': [
            'yase=yase.main:main',
        ],
    }
)
