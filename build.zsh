#!/usr/bin/env zsh

project="IconSetBuilder"

# Punt if there are no arguments
if [ -z "$1" ]; then
	echo "Usage: build.zsh <release | debug>"
	return 0
else
	target=$1
fi

# Build parameters
src_path="build/src"
rel_path="build/release"
dbg_path="build/debug"

if [ $target = "release" ]; then
	target_path=$rel_path
elif [ $target = "debug" ]; then
	target_path=$dbg_path
else
	echo "Unknown build target '${target}'"
	return
fi

echo "Building ${project} target: ${target}"
echo "  source path: ${src_path}"
echo "  target path: ${target_path}"
mkdir -p $src_path
mkdir -p $target_path

function md2txt () {
	if [ -z "$1" ]; then
		echo	"Usage: md2txt <input_markdown_file> [output_text_file]"
		return 0
	fi
	if [ -z "$2" ]; then
		fbase=$(basename "$1")
		fname="${fbase%.*}"
		pandoc -f markdown -t plain $1 -o "${fname}.txt"
	else
		pandoc -f markdown -t plain $1 -o $2
	fi
}

# target source
rsync -u -r *.py "${src_path}/lib/"
rsync -u scripts/src/${target}/* "${src_path}/"
rsync -u -r doc "${src_path}/"
rsync -u -r resources "${src_path}/"
rsync -u README.md "${src_path}/"

# target examples
rsync -u -r example "${src_path}/"

# target configuration
rsync -u -r scripts/config/${target}/* "${target_path}/"
rsync -u INSTALL.md "${target_path}/"

# convert md to txt for the markdown impaired
md2txt README.md "${src_path}/doc/README.txt"
pushd "${src_path}/doc"
for mdfile in *.md; do md2txt "${mdfile}"; done
popd

# Create the target archive
echo -e "  creating ${target} target archive ${project}.zip"
pushd "${src_path}"
zip -r -q "../${target}/${project}.zip" *
popd

# Create direnv environment for build
# Necessary for the script to use the local lib for package
# dependencies rather than the parent dir global package environment
#
rsync -u .conf/envrc build/.envrc
cd build
sleep 2
direnv allow

echo Done.

