"""

    Reynir: Natural language processing for Icelandic

    CFFI builder for _trie module

    Copyright (C) 2019 Miðeind ehf.
    Original author: Vilhjálmur Þorsteinsson

       This program is free software: you can redistribute it and/or modify
       it under the terms of the GNU General Public License as published by
       the Free Software Foundation, either version 3 of the License, or
       (at your option) any later version.
       This program is distributed in the hope that it will be useful,
       but WITHOUT ANY WARRANTY; without even the implied warranty of
       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
       GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.


    This module only runs at setup/installation time. It is invoked
    from setup.py as requested by the cffi_modules=[] parameter of the
    setup() function. It causes the _trie.*.so CFFI wrapper library
    to be built from its source in trie.cpp.

"""

import os
import platform
import cffi

# Don't change the name of this variable unless you
# change it in setup.py as well
ffibuilder = cffi.FFI()

_PATH = os.path.dirname(__file__) or "."
WINDOWS = platform.system() == "Windows"

# What follows is the actual Python-wrapped C interface to trie.*.so

declarations = """

    typedef unsigned int UINT;
    typedef uint8_t BYTE;
    typedef uint32_t UINT32;

    UINT mapping(const BYTE* pbMap, const BYTE* pbWord);
    UINT bitselect(const BYTE* pb, UINT n);
    UINT retrieve(const BYTE* pb, UINT nStart, UINT n);
    UINT lookupFrequency(const BYTE* pb, UINT nQuantumSize, UINT nIndex);
    UINT lookupMonotonic(const BYTE* pb, UINT nQuantumSize, UINT nIndex);
    UINT lookupPartition(const BYTE* pb, UINT nOuterQuantum, UINT nInnerQuantum, UINT nIndex);

"""

# Do the magic CFFI incantations necessary to get CFFI and setuptools
# to compile trie.cpp at setup time, generate a .so library and
# wrap it so that it is callable from Python and PyPy as _trie

if WINDOWS:
    extra_compile_args = ["/Zc:offsetof-"]
else:
    extra_compile_args = ["-std=c++11"]

ffibuilder.set_source(
    "icegrams._trie",
    # trie.cpp is written in C++ but must export a pure C interface.
    # This is the reason for the "extern 'C' { ... }" wrapper.
    'extern "C" {\n' + declarations + "\n}\n",
    source_extension=".cpp",
    sources=["src/icegrams/trie.cpp"],
    extra_compile_args=extra_compile_args,
)

ffibuilder.cdef(declarations)

if __name__ == "__main__":
    ffibuilder.compile(verbose=False)
