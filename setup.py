from setuptools import setup

setup(
    name='mvgrpfiles',
    version='1.0',
    description='A simple Python program',
    author='Guillermo García Grao',
    author_email='guillermo.garcia.grao@gmail.com',
    py_modules=['groups', 'archive'],
    entry_points={
        'console_scripts': [
            'mvgrpfiles = mvgrpfiles'
        ]
    },
)