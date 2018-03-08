rm -Rf build/
rm -Rf dist/
python setup.py build -e "/usr/bin/env python3" sdist bdist_wheel
