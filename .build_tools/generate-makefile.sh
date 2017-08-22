#!/bin/bash

script_path=$(readlink -f $0)
script_directory=$( dirname "${script_path}" )
script_name=$( basename "${script_path}" )

target_root_directory="${1:-${PWD}}"
target_root_directory="${target_root_directory%/}"
target_root_directory="${target_root_directory%/.build_tools}"
if [[ ! -d "${target_root_directory}" ]]; then
	printf "%s: target directory: \"${target_root_directory}\" doesn't exist\n" "${script_name}" >&2
	exit 1
fi
target_makefile="${target_root_directory}/Makefile"

if [[ ! -d "${target_root_directory}" ]]; then
	printf "%s: target directory: \"${target_root_directory}\" doesn't exist\n" "${script_name}" >&2
	exit 1
fi

function create_makefile_variable()
{
	local variable_name="${1}" filetype="${2}" directory="${3}" \
		source_file
	local -a source_files

	while IFS=  read -r -d $'\0'; do
		source_files+=( "${REPLY}" )
	done < <(find "${directory}" -type f -name "*.${filetype}" -print0 2>/dev/null)
	if ((${#source_files[@]} == 1)); then
		source_file="${source_files[0]}"
		printf "${variable_name} = %s" "${source_file#./}"
	elif ((${#source_files[@]} > 1)); then
		printf "%s" "${variable_name} ="
		for source_file in "${source_files[@]}"; do
			printf ' \\\n\t%s' "${source_file#./}"
		done
	fi
	printf "\n\n"
}

truncate -s 0 "${target_makefile}"

create_makefile_variable "MENU_FILES" "menu" "${target_root_directory}" >>"${target_makefile}"

create_makefile_variable "DESKTOP_FILES" "desktop" "${target_root_directory}" >>"${target_makefile}"

create_makefile_variable "DIRECTORY_FILES" "directory" "${target_root_directory}" >>"${target_makefile}"

create_makefile_variable "ICONS" "svg" "${target_root_directory}" >>"${target_makefile}"

create_makefile_variable "WINE_ICO" "ico" "${target_root_directory}" >>"${target_makefile}"

printf "%s\n\n" 'all: $(MENU_FILES) $(DESKTOP_FILES) $(DIRECTORY_FILES) $(ICONS) $(WINE_ICO)' >>"${target_makefile}"

printf "%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n" \
	'install: all' \
	'install -d "$(DESTDIR)$(EPREFIX)/etc/xdg/menus/applications-merged"' \
	'install -m0644 $(MENU_FILES) "$(DESTDIR)$(EPREFIX)/etc/xdg/menus/applications-merged"' \
	'install -d "$(DESTDIR)$(EPREFIX)/usr/share/applications"' \
	'install -m0644 $(DESKTOP_FILES) "$(DESTDIR)$(EPREFIX)/usr/share/applications"' \
	'install -d "$(DESTDIR)$(EPREFIX)/usr/share/desktop-directories"' \
	'install -m0644 $(DIRECTORY_FILES) "$(DESTDIR)$(EPREFIX)/usr/share/desktop-directories"' \
	'install -d "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/apps"' \
	'install -m0644 icons/hicolor/scalable/apps/* "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/apps"' \
	'install -d "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/places"' \
	'install -m0644 icons/hicolor/scalable/places/* "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/places"' \
	'install -d "$(DESTDIR)$(EPREFIX)/usr/share/wine/icons"' \
	'install -m0644 $(WINE_ICO) "$(DESTDIR)$(EPREFIX)/usr/share/wine/icons"' >>"${target_makefile}"


