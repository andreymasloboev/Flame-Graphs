cmake_minimum_required(VERSION 3.20)

project (Coverage VERSION 0.1 DESCRIPTION "Sample build code coverage with google tests")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Debug" CACHE STRING "Debug was set by default" FORCE)
endif()

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

include(CMakeDependentOption)
option(WITH_TESTS "Build with tests" ON)

set(HDR_FILES
    include/resource.hpp
)

set(SRC_FILES
    src/resource.cpp
)

set(SRC_MAIN_FILES
    src/main.cpp
)

add_library(${PROJECT_NAME}_lib ${SRC_FILES} ${HDR_FILES})
target_include_directories(${PROJECT_NAME}_lib PUBLIC include)

add_executable(${PROJECT_NAME} ${SRC_MAIN_FILES})
target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_NAME}_lib)


if (WITH_TESTS)
  find_package(GTest REQUIRED)
  enable_testing()
  add_subdirectory(tests)
endif()

include(CMakePrintHelpers)
message(STATUS "=======================================")
message(STATUS "Configured project: ${PROJECT_NAME}")
message(STATUS "======= Project variables =============")
cmake_print_variables(CMAKE_C_FLAGS)
cmake_print_variables(CMAKE_CXX_FLAGS)