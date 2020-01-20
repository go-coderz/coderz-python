#/bin/bash

source ENV/bin/activate                                                                 

python3 setup.py sdist bdist_wheel
pip3 install dist/coderz-0.1.2.tar.gz
