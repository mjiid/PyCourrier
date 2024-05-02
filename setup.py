from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='PyCourrier',
    version='0.1.6',
    packages=find_packages(),
    description='A simple email sender utility',
    author='Abdelmajid Habouch',
    author_email='Habush1610@gmail.com',
    url='https://github.com/mjiid/PyCourrier',
    license='MIT',
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
