from setuptools import setup

setup(
    name='mvgrpfiles',
    version='1.0.1',
    description='A Python program that moves all files from all members of a group to an archive',
    author='Guillermo García Grao',
    author_email='guillermo.garcia.grao@gmail.com',
    # py_modules=['groups', 'archive'],
    packages=["mvgrpfiles"],
    entry_points={
        'console_scripts': [
            'mvgrpfiles = mvgrpfiles.__main__:main'
        ]
    },
)
