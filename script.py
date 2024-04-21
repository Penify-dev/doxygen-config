import subprocess
import os

def install_packages():
    subprocess.run(["pip", "install", "sphinx", "breathe"], check=True)

def setup_doxygen(source_dir, output_dir):
    # Change these paths as needed
    doxyfile_content = f"""
PROJECT_NAME = "My Project"
INPUT = "{source_dir}"
OUTPUT_DIRECTORY = "{output_dir}/docs"
GENERATE_XML = YES
XML_OUTPUT = xml
RECURSIVE = YES
INPUT = {source_dir}/xeno\ rat\ client {source_dir}/xeno\ rat\ server {source_dir}/Plugins
    """
    doxyfile_path = os.path.join(output_dir, "Doxyfile")
    with open(doxyfile_path, "w") as file:
        file.write(doxyfile_content)

    # Run Doxygen
    subprocess.run(["doxygen", doxyfile_path], check=True)

def setup_sphinx(source_dir, output_dir):
    # Sphinx project directory
    docs_dir = os.path.join(output_dir, "sphinx-docs")
    os.makedirs(docs_dir, exist_ok=True)

    # Initialize Sphinx
    subprocess.run(["sphinx-quickstart", "--quiet", "--project", "My Project",
                    "--author", "Your Name", "--sep", "-p", ".", "-a", ".", "-r", ".", "-l", "en",
                    "--ext-autodoc", "--ext-todo", "--ext-coverage", "--ext-imgmath", "--ext-mathjax",
                    "--ext-ifconfig", "--ext-viewcode", "--makefile", "--batchfile", "--no-use-make-mode"],
                   cwd=docs_dir, check=True)

    # Configure Breathe in Sphinx's conf.py
    conf_path = os.path.join(docs_dir, "conf.py")
    with open(conf_path, "a") as conf_file:
        conf_file.write(f"""
import os
import sys
extensions = ['breathe']

# Breathe configuration
breathe_projects = {{ 'MyProject': '../xml' }}
breathe_default_project = 'MyProject'
html_theme = 'sphinx_rtd_theme'
""")

    # Build Sphinx
    subprocess.run(["sphinx-build", "-b", "html", ".", "_build/html"], cwd=docs_dir, check=True)

def main():
    install_packages()
    source_dir = "/Users/sumansaurabh/Documents/my-startup/xeno-rat"  # Set your source directory
    output_dir = "/Users/sumansaurabh/Documents/my-startup/docs-xeno-rat/"  # Set your output directory

    setup_doxygen(source_dir, output_dir)
    # setup_sphinx(source_dir, output_dir)

if __name__ == "__main__":
    main()
