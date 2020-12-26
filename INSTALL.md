# Directory Opus Icon Set Builder Installation

## Overview

This app automates the process of building a custom Directory Opus iconset. The input to the script is a configuration file in either `JSON` or `YAML` format, accompanied by a set of "large"icon image files and another set of "small" icon image files as used by Directory Opus. The output from the script is a `.dis iconset bundle` that is loaded into Directory Opus via `Preferences->Toolbars->Icons`. In addition to creating the iconset .dis bundle, the script can also generate all the intermediate files that make up that bundle, resize disparate icons to make them compatible with DOpus, add padding to icons and more.

## Distribution

This distribution is comprised of three files:

- **INSTALL.md** (this file)
- **IconSetBuilder.zip**: this archive contains all content necessary to run the app.
- **install.cmd**: this batch file will extract the `IconSetBuilder.zip` file and setup the necessary runtime environment. At its core, the app runs a Python script, so it is necessary to have Python 3 installed in advance. Follow the installation instructions below regarding Python installation <u>before</u> running this batch file.

## Installation

1. **IMPORTANT:** <u>Install Python 3 first</u>! Fortunately, Microsoft made this easy, as you can install Python 3 directly from the [Microsoft Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7?activetab=pivot:overviewtab). Or, if you prefer, you can also download the latest Python 3 version from the  [Official Python website](https://www.python.org/downloads/windows/). In either case, make sure you install `Python v.3.9 or later`. <u>Do not install or use Python 2 as this will cause things to fail</u>. You can check the Python version by running `python --version`.
2. Now, to get things up and running, execute the installer `install.cmd` from a cmd prompt. This will extract the `IconSetBuilder` app folder and setup the Python environment automatically so you don't need to deal with any Python related details.
3. Read `README.md` in the IconSetBuilder folder for detailed information on configuration and usage.

