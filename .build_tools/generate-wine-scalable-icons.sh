#!/bin/bash

script_path=$(readlink -f $0)
script_directory=$( dirname "${script_path}" )
script_name=$( basename "${script_path}" )

declare -a source_app_icons=( "programs/notepad/notepad.svg"
							"programs/taskmgr/taskmgr.svg"
							"programs/regedit/regedit.svg"
							"programs/msiexec/msiexec.svg"
							"programs/winecfg/winecfg.svg"
							"programs/winefile/winefile.svg"
							"programs/winemine/winemine.svg"
							"programs/cmd/wcmd.svg"
							"programs/iexplore/iexplore.svg"
							"programs/winhlp32/winhelp.svg"
							"programs/wordpad/wordpad.svg" )
declare -a source_places_icons=( "dlls/shell32/document.svg"
								"dlls/shell32/mydocs.svg"
								"dlls/shell32/desktop.svg"
								"dlls/shell32/printer.svg"
								"dlls/shell32/drive.svg"
								"dlls/shell32/control.svg"
								"dlls/shell32/cdrom.svg"
								"dlls/shell32/netdrive.svg"
								"dlls/shell32/mycomputer.svg" )

declare wine_logo_icon="wine.svg"


function git_update_wine()
{
	local working_directory="${1}"

	pushd "${working_directory}"
	git pull
	git checkout origin/master
	git reset --hard origin/master
	popd
}

if [[ -n "${1}" ]]; then
	working_directory="${1}"
else
	temporary_directory=$(mktemp -d "wine-git.XXXXXXXXXX")
	working_directory="${temporary_directory}"
fi
working_directory="${working_directory%/}"


if [[ -n "${2}" ]]; then
	target_root_directory="$(readlink -f "${2}")"
else
	target_root_directory="${PWD}"
fi
target_root_directory="${target_root_directory%/}"
target_root_directory="${target_root_directory%/.build_tools}"

if [[ ! -d "${working_directory}" ]]; then
	printf "%s: Wine .git directory: \"%s\" doesn't exist\n" "${script_name}" "${working_directory}" >&2
	exit 1
fi
if [[ ! -d "${target_root_directory}" ]]; then
	printf "%s: target directory: \"%s\" doesn't exist\n" "${script_name}" "${target_root_directory}" >&2
	exit 1
fi

if [[ ! -d "${working_directory}/.git" ]]; then
	git clone "https://source.winehq.org/git/wine.git" "${working_directory}/wine"
	working_directory="${working_directory}/wine"
fi

git_update_wine "${working_directory}"

if [[ -d "${target_root_directory}/icons/hicolor/" ]]; then
	rm -rf "${target_root_directory}/icons/hicolor/"
fi
mkdir -p "${target_root_directory}/icons/hicolor/scalable/"{apps,places}

target_path="${target_root_directory}/icons/hicolor/scalable/apps/${wine_logo_icon}"
wine_icon_path="${target_path}"
	awk -vtarget_path="${target_path}" -f "${target_root_directory}/.build_tools/clone_and_overlay_wine_logo.awk" \
			"${working_directory}/dlls/user32/resources/oic_winlogo.svg"
#clone_old_style_icon "${working_directory}/dlls/user32/resources/oic_winlogo.svg" "${target_path}"

for icon_rpath in "${source_app_icons[@]}"; do
	icon="$(basename "${icon_rpath}")"
	icon="wine-${icon}"
	echo "Processing icon: ${icon} ..."
	target_path="${target_root_directory}/icons/hicolor/scalable/apps/${icon}"
	awk -vtarget_path="${target_path}" -f "${target_root_directory}/.build_tools/clone_and_overlay_wine_logo.awk" \
			"${working_directory}/${icon_rpath}"
done

for icon_rpath in "${source_places_icons[@]}"; do
	icon="$(basename "${icon_rpath}")"
	icon="${icon%.svg}-wine.svg"
	echo "Processing icon: ${icon} ..."
	target_path="${target_root_directory}/icons/hicolor/scalable/places/${icon}"
	awk -vtarget_path="${target_path}" -f "${target_root_directory}/.build_tools/clone_and_overlay_wine_logo.awk" \
		"${wine_icon_path}" "${working_directory}/${icon_rpath}"
done

[[ -n "${temporary_directory}" && -d "${temporary_directory}" ]] && rm -rf "${temporary_directory}"
