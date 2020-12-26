# Directory Opus Icon Set Builder

This app automates the process of building a custom Directory Opus iconset. The input to the script is a configuration file in either `JSON` or `YAML` format, accompanied by a set of "large"icon image files and another set of "small" icon image files as used by Directory Opus. The large and small icon Images are typically sized to 32 and 24 pixels respectively. The output from the script is a `.dis iconset bundle` that is loaded into Directory Opus via `Preferences->Toolbars->Icons`. In addition to creating the iconset .dis bundle, the script can also generate all the intermediate files that make up that bundle, resize disparate icons to make them compatible with DOpus, add padding to icons and more.

At its core, this app is a Python script `IconSetBuilder.py`that is invoked by running `IconSetBuilder.cmd`which sets up the Python environment and passes on the relavent command line arguments. See below for usage details.

To get things up and running, execute the installation batch file` install.cmd` from a cmd prompt. This will setup the Python environment and all the necessary python dependencies automatically so you don't need to deal with those details. The only thing you need to do beforehand is install a suitable Python 3 distribution. Fortunately, Microsoft made that easy, as you can install Python 3 directly from the [Microsoft Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7?activetab=pivot:overviewtab).

In order to understand how this app works and what you can do with it, please read through the docs and review the included example content which can be used as a guide and template for creating your own configuration.

## Requirements

|          Requirement          | Description                                                  |
| :---------------------------: | ------------------------------------------------------------ |
|           Python 3            | If you don't already have Python 3 installed on your system, you can install`Python v.3.9` from the [Microsoft Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7?activetab=pivot:overviewtab). If you already have python installed, make sure to upgrade to Python v.3.9 or higher either from the Microsoft Store or the [Official Python website](https://www.python.org/downloads/windows/). Make sure that you are not running Python 2 as this will cause things to fail. You can verify your Python version by running `python --version`. |
| Python Package   Dependencies | Required Python package dependencies are handled automatically by this app. When you run `install.cmd`, the batch file creates a local Python 3 environment and installs the necessary packages there. When you run `IconSetBuilder.cmd` to create an iconset, the batch file loads that local Python environment and executes the script within it. You do not have to deal with manually setting up anything Python related. |
|  Icon Set Configuration File  | You will need to create a configuration file for your icon set in either `JSON` or `YAML` format. Use the provided example `iconset.json` and `iconsetcfg.yaml` files located in the example folder as a template. Note that YAML has some formatting requirements that are listed in the `Caveats` section below. |
|             Icons             | You will need to create a set of icons for both the large and small icons used in Directory Opus. These icon files should preferably be in `.png` format, but `.jpg, .jpeg and .gif` formats will also work. The icons should be sized to `32 and 24 pixels` and located in separate folders. The included example icons are stored in `icons\32 and icons\24` but these names are not cut in stone. The folder names can be whatever you wish, but they should at least hint at the size of the icons. Another possibile option might be `icons\large and icons\small`. |

## Input and Output Files

#### Input

- **Iconset configuration file:** (see below) must be in either JSON or YAML format. Use the example `iconsetcfg.json` and `iconsetcfg.yaml` files as templates for creating your own configuration file.
- **Icons:** two folders containing the `large` and `small` icon images needed to build the iconset; typically `32` and `24` pixels respectively. Review the example icons  and read the additional document`DOpus Default Icon Names.md`for tips on naming your icons.

#### Output

**Iconset .dis bundle**: this is simply a `.zip`archive renamed to `.dis`. After building the .dis file, these individual files are removed unless the `-i / --intfiles` option is supplied. Retaining the intermediate files is useful for reviewing/verifying the icon set content without having to extract the bundle file. The .dis bundle contains the following:

- Icon set definitions file: [icon set name].xml
- Large icon sheet: [icon set name]-large-iconset.png
- Small icon sheet: [icon set name]-small-iconset.png

<u>Note</u>: the term `icon sheet` refers to a single image containing  a 32 column grid of individual icons. The icon set definitions file [icon set name].xml references individual icons in this image sheet by their row x col position in the grid.

## The Icon Set Configuration File

Both JSON and YAML configuration file formats are supported by this app. There is no advantage to using one format over the other so the choice is strictly a personal preference. In either case, the required sections and parameters for the configuration file are shown below.

<img src="resources/media/iconsetcfg-sections.png" alt="Iconset Configuration File Structure"  />

## Installation and Configuration

1. Install Python 3 from the  [Microsoft Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7?activetab=pivot:overviewtab) or from the  [official Python website](https://www.python.org/downloads/windows/).
2. Run the installer `install.cmd` included in this distribution. This will extract the `IconSetBuilder.zip` archive, install the necessary Python environment, and change directory to the extracted folder.
3. Read the documentation: This `README.md` file and the `DOpus Default Icon Names.md` file  located in the doc folder.
4. Review the example configuration files `iconsetcfg.json` and `iconsetcfg.yaml`as well as the sample icons located in the example folder.
5. Review the example output files located in the example/output folder.
6. Generate the example content by running `IconSetBuilder.cmd -i example\iconsetcfg.json`. This will generate the example iconset bundle named `X-Qute Test IconSet (JSON).dis` and the intermediate .png and .xml files that comprise that bundle. Review that output.
7. Create a set of large and small icons, each in their own subfolder (ex. icons\large and icons\small or icons\32 and icons\24).
8. Using the examples as a guide, create an iconset configuration file based on the icons created in step 7. Creating the `names` sections for the icons is optional.
9. Review the Usage section below and run the IconSetBuilder.cmd script to create your iconset .dis bundle.
10. Open Directory Opus Preferences, navigate to the `Toolbars->Icons` section and select `Import` to load your iconset.
11. Have at it!

<img src="resources/media/dopus-iconset-prefs.png" alt="DOpus IconSet Preferences"  />

   ### Optional:

When executed, `IconSetBuilder.cmd` automatically loads the necessary Python 3 environment required to run the script and unloads that environment upon completion. If you wish to see how things work under the hood, you can manually load the Python environment by executing the batch file `lib\python\Scripts\activate.bat`. Conversely, to unload the Python environment, execute the batch file `lib\python\Scripts\deactivate.bat`.

## Usage

`IconSetBuilder.cmd [-h] [-i] [-r] [-m <margin>] [-p <padding>] [-f] configfile`

Minimal usage: `IconSetBuilder.cmd <configfile>`

| Short Arguments | Full Arguments       | Description                                                  |
| --------------- | -------------------- | ------------------------------------------------------------ |
| ...             | `<configfile>`       | icon set configuration file (JSON or YAML)                   |
| `-f`            | `--deficons`         | include default empty and spacer icons                       |
| `-i`            | `-intfiles`          | generate intermediate files used to build the ".dis" bundle. This option<br /> is useful for verifying the content of the ".dis" bundle |
| `-r`            | `--resize`           | resize icons to the default values specified in the `iconsize` parameter<br />in the configuration file |
| `-m <pixels>`   | `--margin <pixels>`  | icon sheet margin size in pixels (default =0 )               |
| `-p <pixels>`   | `--padding <pixels>` | icon padding in pixels (default = 0)                         |
| `-h`            | `--help`             | show usage information and exit                              |

## Examples

Following are some example usage scenarios:

```
IconSetBuilder.cmd configfile.json
```

- Basic usage: creates an icon set .dis bundle based on the provided configuration file

```
IconSetBuilder.cmd -i configfile.json
```

- Creates an icon set .dis bundle along with the intermediate bundled content. The intermediate files are useful for verifying the icon set without having to extract the .dis file.

```
IconSetBuilder.cmd -f configfile.json
```

- Creates an icon set .dis bundle that includes the empty and spacer icons that are part of a standard DOpus icon set

```
IconSetBuilder.cmd -i -f configfile.json
```

- Creates an icon set .dis bundle with intermediate content that also includes the empty and spacer icons

```
IconSetBuilder.cmd -r configfile.json
```

- Resizes icons to default values for the large and small icon sets; typically 32 and 24 pixels respectively. This option should be used when you are working with icons of varied sizes that need to normalized to those defaults.

```
IconSetBuilder.cmd -m 8 configfile.json
```

- Creates an icon set .dis bundle with an icon sheet image margin of 8 pixels

```
IconSetBuilder.cmd -p 2 configfile.json
```

- Creates an icon set .dis bundle that adds 2 pixel padding to each icon

```
IconSetBuilder.cmd -h
```

- Displays the usage information for the app

## Icon Names

Names can be assigned to individual icons in one of two ways:

- **Names List (optional)**: include a list of names in the configuration file under the `names` section for each of the large and small icon sets. The `names` list length should match one-to-one with the `icons` list length. If there is a difference between the two, the script will quit with an error.
- **Automatic Naming (default)**: if the `names` section for the large and small sets are not specified in the configuration file, the script will "auto-create" icon names derived from the icon filenames themselves by replacing underscores and dashes with spaces and then applying title-case to the individual words in the name (ex.my-icon-file.png will result in the name My Icon File.)

**Consideration**: you can use whatever names you wish for your icons, but it is worthwhile to consider using the naming convention established for standard DOpus iconsets. This convention does two things: 1) it defines an ordered list of icon names that corresponding to specific DOpus commands and 2) references icons that visually correspond to the meaning of those commands. The order of the names in the list correspond to the row x col position of  icons in the iconset master image grid (icon sheet). If you wish to follow that convention, see `Default Icon Names.md` in the doc folder for details,

## Caveats

- `YAML file format:` Line indentation must use spaces and not tabs. This is a YAML formatting requirement (it does not apply to JSON). If you have inadvertently used tabs or end up with a mix of tabs and spaces, there are quite a few good online converters that will heal your woes. Do a Google search on "spaces tabs online converter". Here's one such converter on [browserling](https://www.browserling.com/tools/tabs-to-spaces).

- `Then why include YAML?` The answer is that YAML format is easier to read than JSON (according to this humble developer)  and, if you follow the remedy to the previous caveat, is easier to create. There are no curly braces and double quotes and commas.

## GitHub

This project can be found on GitHub at [Directory Opus IconSet Builder](https://github.com/mark-ingenosity/DOpus-IconSetBuilder)

