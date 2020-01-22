import setuptools
#print(setuptools.find_packages(where='src'))
#exit()
with open("Readme.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='coderz',
    version='0.1.5',
    author="CoderZ",
    author_email="app@gocoderz.com",
    python_requires='>3.0',
    description="CoderZ External IDE Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/go-coderz/coderz-python",
    install_requires=[
    'websockets>=7.0',
    'python-socketio==4.0.2',
    'aiohttp>=3.0.0'
    ],
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'': ['*']},
    include_package_data=True,
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
