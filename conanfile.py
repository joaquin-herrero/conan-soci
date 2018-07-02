from conans import ConanFile, CMake, tools


class SociConan(ConanFile):
    name = "soci"
    version = "3.2.3"
    license = "Boost Software License"
    url = "https://github.com/SOCI/soci"
    description = "Originally, SOCI was developed by Maciej Sobczak at CERN as abstraction layer for Oracle, a " \
                  "Simple Oracle Call Interface. Later, several database backends have been developed for SOCI, " \
                  "thus the long name has lost its practicality. Currently, if you like, SOCI may stand for " \
                  "Simple Open (Database) Call Interface or something similar."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "tests": [True, False], "sanitizer": [True, False]}
    default_options = "shared=True", "tests=False", "sanitizer=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/SOCI/soci.git")
        self.run("cd soci && git checkout master")
        tools.replace_in_file("soci/CMakeLists.txt", "project(SOCI)", """project(SOCI)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

        tools.replace_in_file("soci/cmake/SociConfig.cmake", """set(SOCI_CXX_VERSION_FLAGS "-std=c++11")""", """set(SOCI_CXX_VERSION_FLAGS "-std=c++14")""")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["SOCI_SHARED"] = self.options.shared
        cmake.definitions["SOCI_STATIC"] = not self.options.shared
        cmake.definitions["SOCI_TESTS"] = self.options.tests
        cmake.definitions["SOCI_ASAN"] = self.options.sanitizer
        cmake.definitions["SOCI_CXX_C11"] = True
        cmake.configure(source_folder="soci")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="soci/include")
        self.copy("*.h", dst="include/soci", src="include/soci")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["soci_core_4_0", "soci_empty_4_0", "soci_odbc_4_0"]