#/bin/bash

source ENV/bin/activate

if ! which pip3 >/dev/null; then
    echo 'pip3 not installed.\nInstall pip3 to continue.'
    exit 1
fi

if ! pip3 list | grep -F wheel >/dev/null; then
    echo "Need to install 'wheel'.\nInstalling"
    pip3 install wheel
fi

python3 setup.py sdist bdist_wheel

echo "Installing coderz using pip3"

pip3 install dist/coderz-0.1.2.tar.gz
