cmake_minimum_required(VERSION 3.11.0)
project(pygraphviz LANGUAGES C CXX)

list(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_SOURCE_DIR}/CMake")

include(skbuild_utils)

find_package(PythonExtensions REQUIRED)

# If a conda prefix is active, default to that
set(GRAPHVIZ_FIND_QUIETLY FALSE)
set(GRAPHVIZ_LIBRARY_PREFIX "$ENV{CONDA_PREFIX}/lib")
set(GRAPHVIZ_INCLUDE_PREFIX "$ENV{CONDA_PREFIX}/include")
find_package(Graphviz)

if (NOT GRAPHVIZ_FOUND)
  message(WARNING "
    1) You don't have Graphviz installed:
       Install Graphviz (http://graphviz.org)

    2) Your Graphviz package might incomplete.
       Install the binary development subpackage (
       e.g. sudo apt install libgraphviz-dev or similar.)

    3) You are using Windows
       There are no PyGraphviz binary packages for Windows but you might be
       able to build it from this source.  See
       http://networkx.lanl.gov/pygraphviz/reference/faq.html
    ")
  message(FATAL_ERROR "Pygraphviz CMakeLists cant find a graphviz installation. Exiting.")
endif()

add_subdirectory("pygraphviz")
