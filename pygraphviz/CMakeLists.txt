find_package(Graphviz)

set(sources "graphviz_wrap.c")
set(module_name "graphviz_wrap")

# Create C++ library. Specify include dirs and link libs as normal
add_library(${module_name} MODULE ${sources})
target_include_directories(${module_name} PUBLIC
  ${PYTHON_INCLUDE_DIRS}
  ${GRAPHVIZ_INCLUDE_DIR}
)
target_link_libraries(${module_name}
  ${PYTHON_LIBRARIES}
  ${GRAPHVIZ_CDT_LIBRARY}
  ${GRAPHVIZ_CGRAPH_LIBRARY}
)
# Transform the C++ library into an importable python module
python_extension_module(${module_name})

# Install the C++ module to the correct relative location
# (this will be an inplace build if you use `pip install -e`)
file(RELATIVE_PATH _install_dest "${CMAKE_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
install(TARGETS ${module_name} LIBRARY DESTINATION "${_install_dest}")
