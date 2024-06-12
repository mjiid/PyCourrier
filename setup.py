from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name='PyCourrier',
    version='0.2',
    packages=find_packages(),
    description='A Python package for sending emails using various SMTP services',
    author='Abdelmajid Habouch',
    author_email='Habush1610@gmail.com',
    url='https://github.com/mjiid/PyCourrier',
    license='MIT',
    install_requires=[
        'asyncio',
        'apscheduler',
        'jinja2',
        'requests',
        'gnupg',
        'sendgrid',
        'gettext',
        'babel',
        'googletrans'
    ],
    extras_require={
        'dev': [
            'pytest',
            'sphinx',
            'sphinx_rtd_theme'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
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
