cmake_minimum_required(VERSION 3.15)
project({{name}} LANGUAGES C VERSION {{version}})

configure_file(
    conf/version.h.in
    ${CMAKE_CURRENT_BINARY_DIR}/conf/version.h
)

set(CMAKE_C_STANDARD 11)

# Enable clangd fix all paths by building project in Debug
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Make root folder the project folder for #FILE macro
set(CMAKE_C_FLAGS "-ffile-prefix-map=${CMAKE_CURRENT_LIST_DIR}/src/=")

{% if requires is defined -%}
{% for require in requires -%}
find_package({{as_name(require)}} CONFIG REQUIRED)
{% endfor %}
{%- endif %}

include_directories(BEFORE ${CMAKE_CURRENT_BINARY_DIR}/conf/ )
include_directories(BEFORE src/ )
include_directories(BEFORE deps/ )

# Strip Release executable
add_link_options($<$<CONFIG:RELEASE>:-s>)

add_executable(test-{{name}} test/test-main.c)
# target_link_libraries(test-{{name}} ...)

add_executable(${PROJECT_NAME} src/main.c)
{% if requires is defined -%}
target_link_libraries({{name}} PRIVATE 
    {% for require in requires -%}
    {{as_name(require)}}::{{as_name(require)}}
    {% endfor %}
)
{%- endif %}
install(TARGETS ${PROJECT_NAME} DESTINATION ${CMAKE_INSTALL_PREFIX}
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )
