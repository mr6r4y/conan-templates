import os
from conan.tools.scm import Git
from conan import ConanFile
from conan.errors import ConanException
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import (
    get,
    copy,
    rmdir,
)


class {{package_name | capitalize}}Connan(ConanFile):
    name = "{{name}}"

    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of mypkg package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    languages = "C"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }

    def layout(self):
        cmake_layout(self, src_folder="src")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def source(self):
        if os.path.exists(os.path.abspath(".git")):
            self.output.wirteln("Repository is cloned. Skipping ..")
            return
        git = Git(self)
        url = self.conan_data["sources"][self.version].get("url")
        commit = self.conan_data["sources"][self.version].get("commit")
        if url is None:
            raise ConanException(
                "Can't find URL of repo from configuration file for %s" % self.version
            )
        git.clone(url=url, target=".")
        if commit is not None and self.version != "master":
            git.checkout(commit=commit)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(
            self,
            "COPYRIGHT",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
        )
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs = ["{{as_name(name)}}",]

    {% if requires is defined -%}
    def requirements(self):
        {% for require in requires -%}
        self.requires("{{ require }}")
        {% endfor %}
    {%- endif %}

    {% if tool_requires is defined -%}
    def build_requirements(self):
        {% for require in tool_requires -%}
        self.tool_requires("{{ require }}")
        {% endfor %}
    {%- endif %}

