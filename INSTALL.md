# Directory Opus Icon Set Builder Installation

## Overview

This app automates the process of building a custom Directory Opus iconset. The input to the script is a configuration file in either `JSON` or `YAML` format, accompanied by a set of "large"icon image files and another set of "small" icon image files as used by Directory Opus. The output from the script is a `.dis iconset bundle` that is loaded into Directory Opus via `Preferences->Toolbars->Icons`. In addition to creating the iconset .dis bundle, the script can also generate all the intermediate files that make up that bundle, resize disparate icons to the sizes specified for the icon set, add padding to icons and more. Note that this is a Python script at heart so Python 3 must be installed before the app is run for the first time. See the Installation section below for details.

## Distribution

This distribution is comprised of two files:

- **INSTALL.md** (this file)
- **IconSetBuilder.zip**: this archive contains all content necessary to setup and run the app.

## Installation

1. **IMPORTANT - Install Python 3 first:** This app is a python script at heart so Python 3 must be installed. Fortunately, Microsoft makes this easy, as you can install Python 3 directly from the [Microsoft Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7?activetab=pivot:overviewtab). Or, if you prefer, you can also download the latest Python 3 version from the  [Official Python website](https://www.python.org/downloads/windows/). In either case, make sure you install `Python v.3.9`or later. <u>Do not install or use Python 2 as this will cause things to fail</u>. You can check the Python version by running `python --version`.
2. Unzip `IconSetBuilder.zip`
3. Run the enclosed`setup.cmd`from a command prompt which configures Python for the app. This is a one time operation and you can safely remove setup.cmd once the configuration is complete.
4. Test the app by generating some example content: from a command prompt, run `IconSetBuilder.cmd -i example\iconsetcfg.json`. This will generate the example iconset bundle named `X-Qute Test IconSet (JSON).dis` and the intermediate .png and .xml files that comprise that bundle. Review the `example\iconsetcfg.json` configuration file and the output.
5. Read the docs:`INSTALL.md`,`README.md` and `doc\Default Icon Names.md` for app details and usage instructions.

## GitHub

This project can be found on GitHub at [Directory Opus IconSet Builder](https://github.com/mark-ingenosity/DOpus-IconSetBuilder)

