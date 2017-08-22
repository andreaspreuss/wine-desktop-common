#!/bin/bash

target_root_directory="${1:-${PWD}}"
target_root_directory="${target_root_directory%/}"
target_root_directory="${target_root_directory%/.build_tools}"
if [[ ! -d "${target_root_directory}" ]]; then
	printf "%s: target directory: \"${target_root_directory}\" doesn't exist\n" "${script_name}" >&2
	exit 1
fi

declare -a wine_locales=( "en" "ar" "bg" "ca" "cs" "da" "de" "el" "eo" "es" "fa" "fi" "fr" "he" "hi" "hr" "hu" "it" "ja" "ko" "lt" "ml" "nl" "pa" "pl" "pt" "pt-BR" "pt-PT" "ro" "ru" "sk" "sl" "sr" "sr-Cyrl" "sr-Latn" "sv" "te" "th" "tr" "uk" "zh" "zh-CN" "zh-TW" )
declare -a windows_translations
declare -a wine_translations

function translate_text()
{
	local text="${1}" locale="${2}" __translation_reference="${3}"
	declare -n __translation="${__translation_reference}"

	__translation="$(trans -no-ansi -no-auto -b -s en -t "${locale}" "${text}" 2>/dev/null)"
	if [ "${__translation}" = "${text}" ]; then
		__translation="$(trans -indent 0 -no-ansi -no-auto -show-languages N -show-dictionary N -show-prompt-message N -show-original N -s en -t "${locale}" "${text}" 2>/dev/null | awk 'END{gsub("(^.*, |\(|\))",""); print $0}')"
	fi
	if [ "${__translation}" = "" ]; then
		__translation="${text}"
	else
		__translation=$(printf "%s\n" "${__translation}" | sed -e 's/Wine/'"${wine_translations[${locale}]}"'/g;s/Windows/'"${windows_translations[${locale}]}"'/g')
		[ "${__translation}" = "" ] && __translation="${text}"
	fi
}

function build_wine_desktop_file()
{
	local name="${1}" comment="${2}" exec="${3}" icon="${4}" terminal="${5}" hidden="${6}" categories="${7}" mime_type="${8:-}" \
			locale translation

	# pre-translate Wine and Windows
	for locale in "${wine_locales[@]}"; do
		[ "${locale}" = "en" ] && continue
		
		translate_text "Windows" "${locale}" "translation"
		windows_translations[${locale}]="${translation}"
		translate_text "Wine" "${locale}" "translation"
		wine_translations[${locale}]="${translation}"
		#printf "[%s] Windows=\"%s\"  Wine=\"%s\"\n" "${locale}" "${windows_translations[${locale}]}" "${wine_translations[${locale}]}" >&2
	done

	# Header
	printf "%s\n" "[Desktop Entry]"

	# Name
	for locale in "${wine_locales[@]}"; do
		if [ "${locale}" = "en" ]; then
			printf "Name=%s\n" "${name}"
		else
			translate_text "${name}" "${locale}" "translation"
			printf "Name[%s]=%s\n" "${locale/-/@}" "${translation}"
		fi
	done

	# Comment
	if [ -n "${comment}" ]; then
		for locale in "${wine_locales[@]}"; do
			if [ "${locale}" = "en" ]; then
				printf "Comment=%s\n" "${comment}"
			else
				translate_text "${comment}" "${locale}" "translation"
				printf "Comment[%s]=%s\n" "${locale/-/@}" "${translation}"
			fi
		done
	fi

	# Exec
	printf "Exec=%s\n" "${exec}"
	
	# Terminal
	printf "Terminal=%s\n" "${terminal}"

	# Type
	printf "Type=Application\n"

	# Icon
	[ -n "${icon}" ] && printf "Icon=%s\n" "${icon}"

	# MimeType
	[ -n "${mime_type}" ] && printf "MimeType=%s\n" "${mime_type}"

	# Hidden
	[ "${hidden}" = "true" ] && printf "Hidden=%s\n" "${hidden}"

	# Category
	printf "Categories=%s\n" "${categories}"
}

function generate_wine_desktop_files()
{
	local wine_desktop_directory="${1}"
	local -a wine_desktop_files=( "wine-browsecdrive" "wine-cmd" "wine-control" "wine-explorer" "wine-iexplore" "wine-notepad" "wine-oleview" "wine-regedit" "wine-taskmgr" "wine-uninstaller" "wine-wineboot" "wine-winecfg" "wine-winefile" "wine-winemine" "wine-winhelp" "wine-wordpad" "wine-msiexec" "wine-mime-msi" )

	for wine_desktop_file in "${wine_desktop_files[@]}"; do
		printf "\nGenerating  \"%s.desktop\" ...\n" "${wine_desktop_file}"

		wine_desktop_path="${wine_desktop_directory}/${wine_desktop_file}.desktop"
		case "${wine_desktop_file#wine-}" in
			browsecdrive)
				build_wine_desktop_file 'Browse C: Drive' 'Browse your virtual C: drive' 'xdg-open "${HOME}/.wine/dosdevices/c:"' 'drive-wine' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			cmd)
				build_wine_desktop_file 'Wine Command interpreter' 'Starts a new instance of the command interpreter CMD' 'wine cmd.exe' 'wine-wcmd' 'true' '' 'Wine;' '' >"${wine_desktop_path}";;

			control)
				build_wine_desktop_file 'Wine Control' 'A clone of the Windows Control Panel' 'wine control.exe' 'control-wine' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			explorer)
				build_wine_desktop_file 'Wine Explorer' 'A clone of Windows Explorer' 'wine explorer.exe' 'wine-winefile' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			iexplore)
				build_wine_desktop_file 'Wine Internet Explorer' 'Builtin clone of Windows Internet Explorer®' 'wine iexplore.exe %U' 'wine-iexplore' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			notepad)
				build_wine_desktop_file 'Wine Notepad' 'A clone of the Windows Notepad Text Editor' 'notepad %f' 'wine-notepad' 'false' '' 'Wine-Programs-Accessories;' '' >"${wine_desktop_path}";;

			oleview)
				build_wine_desktop_file 'Wine OLE/COM Object Viewer' 'Windows Object Linking and Embedding/Component Object Model Object Viewer' 'wine oleview.exe' 'control-wine' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			regedit)
				build_wine_desktop_file 'Wine Registry Editor' 'Wine Registry Editor' 'regedit' 'wine-regedit' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			taskmgr)
				build_wine_desktop_file 'Wine Task Manager' 'A clone of Windows Task Manager' 'wine taskmgr.exe' 'wine-taskmgr' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			uninstaller)
				build_wine_desktop_file 'Uninstall Wine Software' 'A clone of Windows Add and Remove Programs Utility' 'wine uninstaller.exe' 'control-wine' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			wineboot)
				build_wine_desktop_file 'Wine Boot' 'Simulate system reboot/stop' 'wineboot' 'mycomputer-wine' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			winecfg)
				build_wine_desktop_file 'Configure Wine' 'Change general Wine options and application overrides/options' 'winecfg' 'wine-winecfg' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			winefile)
				build_wine_desktop_file 'Wine File Browser' 'A clone of Windows Explorer' 'winefile' 'wine-winefile' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			winemine)
				build_wine_desktop_file 'Wine Minesweeper' 'A clone of the Windows Minesweeper game' 'winemine' 'wine-winemine' 'false' '' 'Game;LogicGame;' '' >"${wine_desktop_path}";;

			winhelp)
				build_wine_desktop_file 'Wine Help' 'A clone of the Windows Help File browser' 'wine winhlp32.exe %f' 'wine-winhelp' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			wordpad)
				build_wine_desktop_file 'Wine Wordpad' 'A clone of the Windows Wordpad Text Editor' 'wine wordpad %f' 'wine-wordpad' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			msiexec)
				build_wine_desktop_file 'Wine Windows Installer' 'Wine installer utility for MSI packages' 'wine msiexec /i %f' 'wine-msiexec' 'false' '' 'Wine;' '' >"${wine_desktop_path}";;

			mime-msi)
				build_wine_desktop_file 'Windows Installer File' '' 'wine %f' '' 'false' 'true' 'Wine;' 'application/x-ole-storage;text/mspg-legacyinfo;' >"${wine_desktop_path}";;
		esac
	done
}

generate_wine_desktop_files "${target_root_directory}/applications"

