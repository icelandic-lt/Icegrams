#!/usr/bin/env bash
# Build the icegrams wheels on the CentOS5 base manylinux1 platform
# This script should be executed inside the Docker container!
# It is invoked indirectly from wheels.sh

# Stop execution upon error; show executed commands
set -e -x

# Create wheels for Python 3.4-3.7
for PYBIN in cp34 cp35 cp36 cp37; do
    "/opt/python/${PYBIN}-${PYBIN}m/bin/pip" wheel /io/ -w wheelhouse/
done

# Create wheels for Python >= 3.8
for PYBIN in cp38; do
	"/opt/python/${PYBIN}-${PYBIN}/bin/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/icegrams-*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Set read/write permissions on the wheels
chmod 666 /io/wheelhouse/*
