from setuptools import setup

setup(
    name='mvgrpfiles',
    version='1.0.6',
    description='A Python program that moves all files from all members of a group to an archive',
    author='Guillermo García Grao',
    author_email='guillermo.garcia.grao@gmail.com',
    # py_modules=['groups', 'archive'],
    packages=["mvgrpfiles"],
    # install_requires=["python_version>'3.9'"],
    entry_points={
        'console_scripts': [
            'mvgrpfiles = mvgrpfiles.__main__:main'
        ]
    },
)
