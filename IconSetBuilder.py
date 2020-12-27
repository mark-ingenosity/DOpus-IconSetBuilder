#!/usr/bin/env python

##-------------------------------------------------------------------------------
## Name:		IconSetBuilder.py
## Purpose:	Automates the creation of custom Directory Opus iconsets
##
## Author: Mark Vlach
## Github: https://github.com/mark-ingenosity
## Copyright: 2020
## License:
## Notes:
##-------------------------------------------------------------------------------
ver = "1.0.0-alpha"

# Import python packages
import os
import sys
import math
import glob
import argparse
import xml.etree.ElementTree as tree
from zipfile import ZipFile
import json
# Packages installed via pip
import dpath.util
from PIL import Image, ImageDraw, ImageOps
from ruamel import yaml
import vkbeautify

###############################################################################
# FUNCTIONS
###############################################################################

# Return the absolute coordinates of the icon bounding box on the icon sheet
# image given the relative icon position, dimensions, margin and padding
def getbbox(position, dimensions, margin, padding):
	row,col = position
	height,width = dimensions
	left = margin + padding + col*(width + 2*padding)
	right = left + width
	upper = margin + padding + row*(height + 2*padding)
	lower = upper + height
	return (left,upper,right,lower)

# Add icon to xml element tree
def addicon(iconset, name, row, col):
	ico = tree.SubElement(iconset, 'icon')
	ico.set('name', name)
	ico.set('row', str(row))
	ico.set('col', str(col))

# Test if file exists and is a member of the iconset file collection
def ismember(outsetdict, file):
	return (file in outsetdict and os.path.exists(outsetdict[file]))

# Get the value of specified item in the iconest configuration
# If the item value is unexpected, then quit
def getConfigVal(config, item, quitflag=True):
	result = dpath.util.values(config, item)
	if not result and quitflag:
		print(f'Error: configuration parameter "{item}" not found. Check parameter syntax in config file.')
		sys.exit(1)
	elif not result and not quitflag:
		return False
	else:
		return result[0]

def validFileExt(param):
	validext=['.json', '.yaml']
	base, ext = os.path.splitext(param)
	if ext.lower() not in validext:
		raise argparse.ArgumentTypeError(f'File type must be one of "{", ".join(validext)}" formats.')
	return param

def validateCfg(configfile, config):
	sections = [
	"/iconsets/parameters/name",
	"/iconsets/parameters/display_name",
	"/iconsets/parameters/copyright",
	"/iconsets/parameters/artist",
	"/iconsets/sets/large/parameters/directory",
	"/iconsets/sets/large/parameters/iconsize",
	"/iconsets/sets/large/icons",
	"/iconsets/sets/large/names",
	"/iconsets/sets/small/parameters/directory",
	"/iconsets/sets/small/parameters/iconsize",
	"/iconsets/sets/small/icons",
	"/iconsets/sets/small/names"
	]

	print(f'Validating configuration file "{configfile}"')

	for section in sections:
		result = dpath.util.values(config, section)
		if not result or not result[0]:
			print(f'Error: section "{section}" not found or enmpty.')
		else:
			print(f'OK: section {section}')

	print('Done.')

###############################################################################
# END FUNCTIONS
###############################################################################

# Build the command line parser and crunch the args
parser = argparse.ArgumentParser(
	description='Directory Opus Iconset Builder %s' % ver
	)
parser.add_argument('configfile', type=validFileExt, help='icon set configuration file')
parser.add_argument('-i', '--intfiles', action='store_true', help='generate intermediate files')
parser.add_argument('-r', '--resize', action='store_true', help='resize icons to defined values')
parser.add_argument('-m', '--margin', metavar='<margin>', default=0, help='icon sheet margin size (default=0)')
parser.add_argument('-p', '--padding', metavar='<padding>', default=0, help='icon padding (default=0)')
parser.add_argument('-f', '--deficons', action='store_true', help='include the default empty and bordered '
					'placeholder icons')
#parser.add_argument('-v', '--validate', action='store_true', help='validate configuration file (default=FALSE)')
args = vars(parser.parse_args())

# Get the configuration file containing the iconset definitions.
configfile = args['configfile']

# Load the configuration file.
# Both .json and .yaml configuration files are supported at the moment.
try:
	if configfile.lower().endswith('.json'):
		iconsetcfg = json.load(open(configfile, 'r'))
	elif configfile.lower().endswith('.yaml'):
		iconsetcfg = yaml.safe_load(open(configfile, 'r'))
	else:
		print(f'Error: invalid file type "{configfile}"')
		parser.print_help(sys.stderr)
		sys.exit(1)
except:
	print(f"Error in {configfile}. Verify content and formatting.")
	sys.exit(1)

# If set, validate the configuration file and exit
#if args['validate']:
#	validateCfg(configfile, iconsetcfg)
#	sys.exit(0)

# Get the iconset content and begin populating the output xml tree
iconsetName = getConfigVal(iconsetcfg, '/iconsets/parameters/name')
iconsetSets = getConfigVal(iconsetcfg, '/iconsets/sets')

# Build the iconset xml headers from the definitions read in from the list file
xmlroot = tree.Element('iconset')
xmlroot.set('name', iconsetName)
display_name = tree.SubElement(xmlroot, 'display_name')
display_name.text = getConfigVal(iconsetcfg, '/iconsets/parameters/display_name')
copyright = tree.SubElement(xmlroot, 'copyright')
copyright.text = str(getConfigVal(iconsetcfg, '/iconsets/parameters/copyright'))
artist = tree.SubElement(xmlroot, 'artist')
artist.text = getConfigVal(iconsetcfg, '/iconsets/parameters/artist')

print(f'Creating iconset "{iconsetName}"')

# Iterate over the sets in the icon list file and construct the
# iconset xml tree and icon sheet image files
for set in iconsetSets:
	directory = getConfigVal(iconsetcfg, f'/iconsets/sets/{set}/parameters/directory')
	height = int(getConfigVal(iconsetcfg, f'/iconsets/sets/{set}/parameters/iconsize'))
	width = int(getConfigVal(iconsetcfg, f'/iconsets/sets/{set}/parameters/iconsize'))
	margin = int(args['margin']) if args['margin'] else 0
	padding = int(args['padding']) if args['padding'] else 0
	# (cmdline option): the number of default icon slots to be added
	ndeficons = 2 if args['deficons'] else 0

	# Get the list of icons and icon names, if specified. If the number of icons
	# does not match the number of names then punt with error message.
	# content to a new list and strip leading and trailing spaces.
	iconlist = getConfigVal(iconsetcfg, f'/iconsets/sets/{set}/icons')
	iconnames = getConfigVal(iconsetcfg, f'/iconsets/sets/{set}/names', False)
	if iconnames and (len(iconlist) != len(iconnames)):
		print(f'Error in configuration file "{configfile}": the number of icons in the '
			f'"{set}" icon set does not match the number icon names')
		sys.exit(1)

	# Begin creation of a transparent icon sheet that is sized correctly for  #
	# the number of icons in the set. This transparent background will        #
	# filled with icons as we later iterate over the rows and columns.        #
	###########################################################################

	# Name the output icon sheet file for the set #
	sheetfile = f'{iconsetName}-{set}-iconset.png'

	# Do all the row and column calculations and sizing for the icon sheet
	# nrows must always be rounded up to the next higher integer value in order
	# to create space for the remainder of icons in the list - int(math.ceil())
	# ensures this. Also, if opticons is set, two additional slots will be added
	# to the list length to accomodate for the two default DOpus empty and
	# spacer icons.
	ncols = 32
	nrows = int(math.ceil((len(iconlist)+ndeficons)/ncols))
	# Calculate the size of the output image, based on the image thumb sizes,
	# margins, and padding
	padw = (ncols-1)*(padding*2)+(padding*2)
	padh = (nrows-1)*(padding*2)+(padding*2)
	marw = margin*2
	marh = margin*2
	msize = (ncols*width)+marw+padw, (nrows*height)+marh+padh

	# Create the correctly sized transparent background image.
	# Note: the last param of the RGBA value controls transparency. Zero means
	# transparent independent of the other values, so the others can be anything
	# e.g. (x,x,x,0)
	sheetimg = Image.new('RGBA', msize, (255,255,255,0))

	# Iterate over the icons list by rows and columns and build the output
	# iconset xml content and icon sheet for the current set
	# -------------------------------------------------------------------------
	iset = tree.SubElement(xmlroot, 'set')
	iset.set('filename', sheetfile)
	iset.set('size', set)
	iset.set('width', str(width))
	iset.set('height', str(height))

	# (cmdline option) creates the default empty and spacer icons
	defaulticons = []
	if args['deficons']:
		emptyicon = Image.new('RGBA', (height, width), (0,0,0,0))
		spacericon = Image.new('RGBA', (height, width), (0,0,0,0))
		ImageDraw.Draw(spacericon).rectangle((0,0,height-1,width-1), outline='gray')
		defaulticons = [['empty',emptyicon], ['spacer',spacericon]]

	for row in range(nrows):
		for col in range(ncols):
			# (cmdline option) insert the default empty and spacer icons
			if defaulticons:
				deficon = defaulticons.pop(0)
				addicon(iset, deficon[0], row, col)
				bbox = getbbox((row,col), (height,width), margin, padding)
				sheetimg.paste(deficon[1], bbox)
				continue

			# Pop icon filenames one at a time from the set's icon list. If icon names
			# are defined for the icon set then then use them, otherwise create clean
			# icon names from the filename (strip underscores and apply titlecase).
			# When the icon filename list is empty, it will throw an expected exception.
			try:
				iconfilename = iconlist.pop(0)
				if iconnames:
					iconname = iconnames.pop(0)
				else:
					iconname = iconfilename.replace('.png','').replace('_',' ').title()
			except:
				break

			# Add the icon to the tree
			addicon(iset, iconname, row, col)

			# Build the icon sheet for the current set
			# -------------------------------------------------------
			# Load the icon file and do one of 1) nothing - pass the icon along
			# as is; 2) resize the icon to hxw as indicated via cmdline arg;
			# 3) add padding to icon as indicated via cmdline arg (note: this
			# will force an icon resize operation to default size + 2 x padding.
			# (ex. new 24 = old 16 + 8 padding)); or 4) exit with errno if icon
			# file is not found.
			iconlocation = directory + '/' + iconfilename
			try:
				iconimg = Image.open(iconlocation)
				# (cmdline option) resize icon to specified hxw
				if (iconimg.size[0] != height) or args['resize']:
					iconimg = iconimg.resize((height, width), Image.ANTIALIAS)
			except:
				print(f'Error: could not open icon file: {iconlocation}. Exiting...')
				sys.exit(1)
			bbox = getbbox((row,col), (height,width), margin, padding)
			try:
				sheetimg.paste(iconimg, bbox)
			except:
				print(f'Mismatch between desired icon size ({height}) and actual image size '
						f'({iconimg.size[0]}). Use the -r switch to resize icons to desired size.')
				sys.exit(1)

	# Cleanup any old files
	for imgFile in glob.glob(f'*{set}-iconset.png'): os.remove(imgFile)

	# Save the icon sheet image file
	sheetimg.save(sheetfile)

# Convert the tree to an xml string
xml = tree.tostring(xmlroot, method='xml', encoding='utf8').decode()

# Beautify and write out the generated xml tree
vkbeautify.xml(xml, f'{iconsetName}.xml')

## Create iconset zipped '.dis' file ##
zf = ZipFile(f'{iconsetName}.zip', mode='w')
zf.write(f'{iconsetName}.xml')
for imgFile in glob.glob('*-iconset.png'): zf.write(imgFile)
zf.close()
if os.path.exists(f'{iconsetName}.dis'): os.remove(f'{iconsetName}.dis')
os.rename(f'{iconsetName}.zip', f'{iconsetName}.dis')

## (--intfiles option) cleanup or keep the intermediate files
if not args['intfiles']:
	print('Cleaning up...')
	os.remove(f'{iconsetName}.xml')
	for imgFile in glob.glob('*-iconset.png'): os.remove(imgFile)
else:
	print("Creating intermediate files...")

print("Done.")
