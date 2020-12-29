#!/usr/bin/env bash

# Build parameters
project="IconSetBuilder"
proj_type="python3"
rel_path="build/release"
dbg_path="build/debug"

# Punt if there are no arguments
if [ -z "$1" ]; then
	echo "Usage: build.zsh <release | debug>"
	exit
else
	target=$1
fi

# Test for correct build command line option and set target path
if ! [[ $target == release || $target == debug ]]; then
	echo "Unknown build target '${target}'"
	exit
fi
target_path="build/${target}"

echo "Building ${project} target: ${target}"
echo "  target path: ${target_path}"
mkdir -p $target_path

# create the temp folder for working files to get zipped
temp_path="${target_path}/temp"
mkdir -p $temp_path

function md2txt () {
	if [ -z "$1" ]; then
		echo	"Usage: md2txt <input_markdown_file> [output_text_file]"
		return 0
	fi
	if [ -z "$2" ]; then
		fbase=$(basename "$1")
		fname="${fbase%.*}"
		pandoc -f markdown -t plain "$1" -o "${fname}.txt"
	else
		pandoc -f markdown -t plain "$1" -o "$2"
	fi
}

# target source
rsync -u -r *.py "${temp_path}/lib/"
rsync -u scripts/src/${target}/* "${temp_path}/"
rsync -u -r doc "${temp_path}/"
rsync -u -r resources "${temp_path}/"
rsync -u README.md "${temp_path}/"

# target examples
rsync -u -r example "${temp_path}/"

# target configuration
rsync -u -r scripts/config/${target}/* "${temp_path}/"
rsync -u INSTALL.md "${target_path}/"

# convert md to txt for the markdown impaired
md2txt README.md "${temp_path}/doc/README.txt"
pushd "${temp_path}/doc" > /dev/null 2>&1
for mdfile in *.md; do md2txt "${mdfile}"; done
popd  > /dev/null 2>&1

# Create the target archive
echo -e "  creating ${target} target archive ${project}.zip"
pushd "${temp_path}" > /dev/null 2>&1
zip -r -q "../${project}.zip" *
popd  > /dev/null 2>&1

# remove the temp files
rm -rf "${temp_path}"

# Optional: if specified, create direnv environment in build.
# This will prevent build from inheriting the project direnv.
#
if [ ! -z "$2" ] && [ "$2" = "direnv" ]; then
	echo "layout_${proj_type}" > build/.envrc
else
 	[ -f build/.envrc ] && rm build/.envrc
 	[ -d build/.direnv ] && rm -rf build/.direnv
fi

echo Done.

