from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name='PyCourrier',
    version='0.1.7',
    packages=find_packages(),
    description='A simple email sender utility',
    author='Abdelmajid Habouch',
    author_email='Habush1610@gmail.com',
    url='https://github.com/mjiid/PyCourrier',
    license='MIT',
    install_requires=[
        'asyncio'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=description,
    long_description_content_type="text/markdown",
)
