#!/usr/bin/env python3.6

""" Module to generate Linux Distribution Agnostic Wine icon, .desktop and .menu data files. """

import argparse
import re
import shutil
import sys
import subprocess
import os
import xml.etree.ElementTree as ElementTree
import copy


GLOBAL_TRANSLATION_DICTIONARY = {"en":{},
                                 "ar":{}, "bg":{},
                                 "ca":{}, "cs":{},
                                 "da":{}, "de":{},
                                 "el":{}, "eo":{}, "es":{},
                                 "fa":{}, "fi":{}, "fr":{},
                                 "he":{}, "hi":{}, "hr":{}, "hu":{},
                                 "it":{}, "ja":{},
                                 "ko":{}, "lt":{}, "ml":{}, "nl":{},
                                 "pa":{}, "pl":{}, "pt":{}, "pt-BR":{}, "pt-PT":{},
                                 "ro":{}, "ru":{},
                                 "sk":{}, "sl":{}, "sr":{}, "sr-Cyrl":{}, "sr-Latn":{}, "sv":{},
                                 "te":{}, "th":{}, "tr":{}, "uk":{},
                                 "zh":{}, "zh-CN":{}, "zh-TW":{}}

# Categories
GLOBAL_WINE_CATEGORIES = {"wine":"X-Wine",
                          "programs":"X-Wine-Programs",
                          "accessories":"X-Wine-Programs-Accessories"}
GLOBAL_GENERAL_CATEGORIES = {"game":"Game", "logic-game":"LogicGame"}

# Desktop launcher files
TYPE = "Application"
GLOBAL_DESKTOP_FILE_DICT = {
    "wine-browsecdrive":{"Name":'Browse C: disk-drive',
                         "Comment":'Browse your virtual C: disk-drive',
                         "Exec":'sh -c "xdg-open $(winepath -u \'C:\' 2>/dev/null)"',
                         "Icon":'drive-wine',
                         "Terminal":"false",
                         "Type":TYPE,
                         "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-cmd":{"Name":'Wine Command interpreter',
                "Comment":'Starts a new instance of the command interpreter CMD',
                "Type":TYPE,
                "Exec":'wine cmd.exe',
                "Icon":'wine-wcmd',
                "Hidden":'true',
                "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-control":{"Name":'Wine Control',
                    "Comment":'A clone of the Microsoft® Windows Control Panel',
                    "Type":TYPE,
                    "Exec":'wine control.exe',
                    "Icon":'control-wine',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-explorer":{"Name":'Wine Explorer',
                     "Comment":'A clone of Microsoft® Windows Explorer',
                     "Type":TYPE,
                     "Exec":'wine explorer.exe',
                     "Icon":'wine-winefile',
                     "Terminal":'false',
                     "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-iexplore":{"Name":'Wine Internet Explorer',
                     "Comment":'Builtin clone of Microsoft® Windows Internet Explorer®',
                     "Type":TYPE,
                     "Exec":'wine iexplore.exe %U',
                     "Icon":'wine-iexplore',
                     "Terminal":'false',
                     "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-notepad":{"Name":'Wine Notepad',
                    "Comment":'A clone of the Microsoft® Windows Notepad Text Editor',
                    "Type":TYPE,
                    "Exec":'notepad %%f',
                    "Icon":'wine-notepad',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"],
                                  GLOBAL_WINE_CATEGORIES["accessories"]]},
    "wine-oleview":{"Name":'Wine OLE/COM Object Viewer',
                    "Comment":('Microsoft® Windows Object Linking and '
                               'Embedding/Component Object Model Object Viewer'),
                    "Type":TYPE,
                    "Exec":'wine oleview.exe',
                    "Icon":'control-wine',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-regedit":{"Name":'Wine Registry Editor',
                    "Comment":'A clone of the Microsoft® Windows Registry Editor',
                    "Type":TYPE,
                    "Exec":'regedit',
                    "Icon":'wine-regedit',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-taskmgr":{"Name":'Wine Task Manager',
                    "Comment":'A clone of Windows Task Manager',
                    "Type":TYPE,
                    "Exec":'wine taskmgr.exe',
                    "Icon":'wine-taskmgr',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-uninstaller":{"Name":'Uninstall Wine Software',
                        "Comment":('A clone of the Microsoft® Windows '
                                   'Add and Remove Programs Utility'),
                        "Type":TYPE,
                        "Exec":'wine uninstaller.exe',
                        "Icon":'control-wine',
                        "Terminal":'false',
                        "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-wineboot":{"Name":'Wine Boot',
                     "Comment":'Simulate system reboot/stop',
                     "Type":TYPE,
                     "Exec":'wineboot',
                     "Icon":'mycomputer-wine',
                     "Terminal":'false',
                     "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-winecfg":{"Name":'Configure Wine',
                    "Comment":'Change general Wine options and application overrides/options',
                    "Type":TYPE,
                    "Exec":'winecfg',
                    "Icon":'wine-winecfg',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-winefile":{"Name":'Wine File Browser',
                     "Comment":'A clone of Microsoft® Windows Explorer',
                     "Type":TYPE,
                     "Exec":'winefile',
                     "Icon":'wine-winefile',
                     "Terminal":'false',
                     "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-winemine":{"Name":'Wine Minesweeper',
                     "Comment":'A clone of the Microsoft® Windows Minesweeper game',
                     "Type":TYPE,
                     "Exec":'winemine',
                     "Icon":'wine-winemine',
                     "Terminal":'false',
                     "Categories":[GLOBAL_WINE_CATEGORIES["wine"],
                                   GLOBAL_GENERAL_CATEGORIES["game"],
                                   GLOBAL_GENERAL_CATEGORIES["logic-game"]]},
    "wine-winhelp":{"Name":'Wine Help',
                    "Comment":'A clone of the Microsoft® Windows Help File browser',
                    "Type":TYPE,
                    "Exec":'wine winhlp32.exe %%f',
                    "Icon":'wine-winhelp',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-wordpad":{"Name":'Wine Wordpad',
                    "Comment":'A clone of the Microsoft® Windows Wordpad Text Editor',
                    "Type":TYPE,
                    "Exec":'wine wordpad %%f',
                    "Icon":'wine-wordpad',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-msiexec":{"Name":'Wine clone of Microsoft® Installer',
                    "Comment":'Wine installer utility for MSI packages',
                    "Type":TYPE,
                    "Exec":'wine msiexec /i %%f',
                    "Icon":'wine-msiexec',
                    "Terminal":'false',
                    "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]},
    "wine-mime-msi":{"Name":'Microsoft® Windows Installer File',
                     "Type":TYPE,
                     "Exec":'wine %%f',
                     "Hidden":'true',
                     "MimeType":["application/x-ole-storage", "text/mspg-legacyinfo"],
                     "Terminal":'false',
                     "Categories":[GLOBAL_WINE_CATEGORIES["wine"]]}
}

# Desktop directory files
GLOBAL_WINE_DESKTOP_FILES = ["Wine", "Wine-Programs", "Wine-Programs-Accessories"]

# Icon File Constants
GLOBAL_NEW_INKSCAPE_VERSION = "0.92"
GLOBAL_NEW_ICON_SIZE = 64
GLOBAL_ICONS_TARGET_RELPATH = "icons/"
GLOBAL_SVG_TARGET_RELPATH = os.path.join(GLOBAL_ICONS_TARGET_RELPATH, "hicolor/scalable/")
GLOBAL_OVERLAY_LARGE_X_SCALE = '0.70'
GLOBAL_OVERLAY_LARGE_Y_SCALE = '0.66'
GLOBAL_OVERLAY_MEDIUM_X_SCALE = '0.48'
GLOBAL_OVERLAY_MEDIUM_Y_SCALE = '0.44'

# Global Wine Logo Overlay icon
GLOBAL_WINE_LOGO_DIRECTORY = "dlls/user32/resources/"
GLOBAL_WINE_SVG_LOGO_FILENAME = "oic_winlogo.svg"
GLOBAL_WINE_ICON_LOGO_FILENAME = "oic_winlogo.ico"

# Application icons
GLOBAL_SVG_APPS_TARGET_RELPATH = os.path.join(GLOBAL_SVG_TARGET_RELPATH, 'apps/')
GLOBAL_APP_SVG_FILES = {'notepad.svg':{'srpath':'programs/notepad/',
                                       'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'taskmgr.svg':{'srpath':'programs/taskmgr/',
                                       'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'regedit.svg':{'srpath':'programs/regedit/',
                                       'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'msiexec.svg':{'srpath':'programs/msiexec/',
                                       'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        GLOBAL_WINE_SVG_LOGO_FILENAME:{
                            'srpath':GLOBAL_WINE_LOGO_DIRECTORY,
                            'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'winecfg.svg':{'srpath':'programs/winecfg/',
                                       'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'winefile.svg':{'srpath':'programs/winefile/',
                                        'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'winemine.svg':{'srpath':'programs/winemine/',
                                        'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'wcmd.svg':{'srpath':'programs/cmd/',
                                    'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'iexplore.svg':{'srpath':'programs/iexplore/',
                                        'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'winhelp.svg':{'srpath':'programs/winhlp32/',
                                       'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH},
                        'wordpad.svg':{'srpath':'programs/wordpad/',
                                       'trpath':GLOBAL_SVG_APPS_TARGET_RELPATH}
                       }

# Place icons
GLOBAL_SVG_PLACES_TARGET_RELPATH = os.path.join(GLOBAL_SVG_TARGET_RELPATH, 'places/')
GLOBAL_PLACES_SVG_FILES = {'document.svg':{'srpath':'dlls/shell32/',
                                           'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH},
                           'mydocs.svg':{'srpath':'dlls/shell32/',
                                         'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH},
                           'desktop.svg':{'srpath':'dlls/shell32/',
                                          'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH},
                           'printer.svg':{'srpath':'dlls/shell32/',
                                          'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH},
                           'drive.svg':{'srpath':'dlls/shell32/',
                                        'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH},
                           'control.svg':{'srpath':'dlls/shell32/',
                                          'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH},
                           'cdrom.svg':{'srpath':'dlls/shell32/',
                                        'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH},
                           'netdrive.svg':{'srpath':'dlls/shell32/',
                                           'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH},
                           'mycomputer.svg':{'srpath':'dlls/shell32/',
                                             'trpath':GLOBAL_SVG_PLACES_TARGET_RELPATH}
                          }

# Global icon id names
GLOBAL_LARGE_SVG_ICON_ID = 'icon:large-scaleable'
GLOBAL_MEDIUM_SVG_ICON_ID = 'icon:medium-scaleable'
GLOBAL_SMALL_SVG_ICON_ID = 'icon:small-scaleable'

# Global SVG namespaces
GLOBAL_XMLNS = {'dc_uri':'http://purl.org/dc/elements/1.1/',
                'cc':'http://creativecommons.org/ns#',
                'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                'xlink':'http://www.w3.org/1999/xlink',
                'sodipodi':'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
                'inkscape':'http://www.inkscape.org/namespaces/inkscape',
                'svg':'http://www.w3.org/2000/svg'}

# Main Directories
GLOBAL_SUBDIRECTORIES = ["applications", "desktop-directories", "icons", "xdg"]


def clean_all(root_directory):
    """ Remove all directories and main Makefile """
    if os.path.exists(root_directory) and os.path.isdir(root_directory):
        for directory in GLOBAL_SUBDIRECTORIES:
            path = os.path.join(root_directory, directory)
            if os.path.isdir(path):
                shutil.rmtree(path)
        path = os.path.join(root_directory, "Makefile")
        if os.path.isfile(path):
            os.unlink(path)


def create_subdirectory(root_directory, subdirectory):
    """ Creates a subdirectory off a give root directory path. """
    directory = os.path.join(root_directory, subdirectory)
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_subdirectories(root_directory):
    """ Create all required subdirectories in target directory. """
    sudirectory_list = GLOBAL_SUBDIRECTORIES
    sudirectory_list += [GLOBAL_SVG_APPS_TARGET_RELPATH, GLOBAL_SVG_PLACES_TARGET_RELPATH]
    for subdirectory in sudirectory_list:
        create_subdirectory(root_directory, subdirectory)


def find_best_translation(search_text, source_text_list):
    """ Accepts a base (English) language string and a source list of translation strings.
    Filters the list of translated strings returning the one with the least matches
    against any words from the base (English) language string."""
    word_list = re.split(' ', search_text)
    lcsearch_text = search_text.lower()
    current_score = len(search_text)
    target_text = ""
    for source_text in source_text_list:
        lcsource_text = source_text.lower()
        if source_text == "":
            continue
        score = 0
        if lcsource_text == lcsearch_text:
            score = len(word_list)
        for word in word_list:
            lcword = word.lower()
            if lcword in lcsource_text:
                score += len(word)
        if score < current_score or target_text == "":
            target_text = source_text
            current_score = score
    return target_text

def translate_text(text, locale):
    """ Translates a block text for the specified locale. Uses shell utility trans. """
    shell_command = 'trans'
    shell_parameters = (f' -indent 0 -no-ansi -no-auto'
                        f' -show-languages N -show-dictionary N -show-prompt-message N'
                        f' -show-original N -s en -t {locale} "{text}"')
    out = subprocess.run(["/bin/bash",
                          "-c",
                          shell_command+shell_parameters],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL,
                         encoding='utf-8')
    if out.returncode != 0:
        raise SystemError(f'Unable to translate "{text}" to locale: {locale}')
    translation_list = re.split(r'\n|, |^\(|\)$', out.stdout, flags=re.MULTILINE)
    translated_text = find_best_translation(text, translation_list)
    return translated_text

def translate_text_lookup(text, locale):
    """ Translate a phrase or word and return result.
        Use a dictionary so subsequent lookups are faster."""
    locale_dictionary = GLOBAL_TRANSLATION_DICTIONARY[locale]
    if locale == "en":
        translated_text = text
    elif not text in locale_dictionary:
        translated_text = translate_text(text, locale)
        locale_dictionary[text] = translated_text
    else:
        translated_text = locale_dictionary[text]
    return translated_text


def create_translated_xdg_entry(entry, content):
    """ Generate the specified XDG file entry with multiple translations. """
    file_text = ""
    for locale in GLOBAL_TRANSLATION_DICTIONARY:
        if locale == "en":
            file_text += f'{entry} = {content}\n'
        else:
            translated_text = translate_text_lookup(content, locale)
            file_text += f'{entry}[{locale}] = {translated_text}\n'
    return file_text


def create_xdg_type_entry(file_content):
    """ Generate a XDG file type entry.
        Also create exec and terminal entries if specified, if is application. """
    file_text = ""
    if file_content["Type"] == "Application":
        # Exec
        if "Exec" in file_content:
            file_text += f'Exec = {file_content["Exec"]}\n'
        # Terminal
        if "Terminal" in file_content:
            file_text += f'Terminal = {file_content["Terminal"]}\n'
    # Type
    file_text += f'Type = {file_content["Type"]}\n'
    return file_text


def create_xdg_file(path, file_content):
    """ Create xdg desktop file @ specified path.
        Use a dictionary of elements."""
    filename = os.path.basename(path)
    print(f'{filename} ', end='')
    sys.stdout.flush()
    file_text = "[Desktop Entry]\n"
    # Name
    if "Name" in file_content:
        file_text += create_translated_xdg_entry("Name", file_content["Name"])
    # Comment
    if "Comment" in file_content:
        file_text += create_translated_xdg_entry("Comment", file_content["Comment"])
    if "Type" in file_content:
        file_text += create_xdg_type_entry(file_content)
    # Icon
    if "Icon" in file_content:
        file_text += f'Icon = {file_content["Icon"]}\n'
    # MimeType
    if "MimeType" in file_content:
        mime_types = ""
        for mime_type in file_content["MimeType"]:
            mime_types += mime_type+";"
        file_text += f'MimeType = {mime_types}\n'
    # Hidden
    if "Hidden" in file_content and file_content["Hidden"]:
        file_text += f'Hidden = {file_content["Hidden"]}\n'
    # Categories
    if "Categories" in file_content:
        categories = ""
        for category in file_content["Categories"]:
            categories += category+";"
        file_text += f'Categories = {categories}\n'
    with open(path, "w") as file_handle:
        file_handle.write(file_text)

def create_wine_desktop_files(directory):
    """ Create all Wine .desktop launcher files. """
    if not os.path.exists(directory):
        os.makedirs(directory)
    for desktop_file in GLOBAL_DESKTOP_FILE_DICT:
        path = os.path.join(directory, desktop_file+".desktop")
        create_xdg_file(path, GLOBAL_DESKTOP_FILE_DICT[desktop_file])


def create_menu_file(directory):
    """ Generate a menu global file, which references custom Wine application Categories """
    def generate_menu_entry(indent, i, names):
        """ Helper to add a nested menu entry to menu file """
        file_text = indent*i+"<Menu>\n"
        file_text += indent*(i+1)+"<Name>"+names[0]+"</Name>\n"
        file_text += indent*(i+1)+"<Directory>"+names[0].lower()+".directory</Directory>\n"
        file_text += indent*(i+1)+"<Include>\n"
        file_text += indent*(i+2)+"<Category>X-"+names[0]+"</Category>\n"
        file_text += indent*(i+1)+"</Include>\n"
        if len(names) > 1:
            file_text += generate_menu_entry(indent, i+1, names[1:])
        file_text += indent*i+"</Menu>\n"
        return file_text
    if not os.path.exists(directory):
        os.makedirs(directory)
    indent = "  "
    i = 1
    entry_type = "Applications"
    file_text = '<!DOCTYPE Menu PUBLIC "-//freedesktop//DTD Menu 1.0//EN"\n'
    file_text += 'http://www.freedesktop.org/standards/menu-spec/menu-1.0.dtd">\n'
    file_text += '<Menu>\n'+indent+'<Name>'+entry_type+'</Name>\n'
    file_text += generate_menu_entry(indent, i, GLOBAL_WINE_DESKTOP_FILES)
    file_text += "</Menu>\n"
    path = os.path.join(directory, GLOBAL_WINE_DESKTOP_FILES[0]. lower()+".menu")
    with open(path, "w") as file_handle:
        file_handle.write(file_text)


def create_wine_menu_files(directory):
    """ Create Wine menu files """
    entry_type = "Directory"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for desktop_file in GLOBAL_WINE_DESKTOP_FILES:
        path = os.path.join(directory, desktop_file.lower()+".directory")
        icon = "wine" if desktop_file == "Wine" else "folder"
        name = re.sub(r'.*\-', r'', desktop_file)
        desktop_file_contents = {"Name":name, "Type":entry_type, "Icon":icon}
        create_xdg_file(path, desktop_file_contents)


def xml_register_svg_ns():
    """ Register all global SVG XML namespaces wtth ElementTree module. """
    for name_space in GLOBAL_XMLNS:
        ElementTree.register_namespace(name_space, GLOBAL_XMLNS[name_space])
        if name_space == 'svg':
            ElementTree.register_namespace('', GLOBAL_XMLNS[name_space])


def xml_svg_load_and_parse(source_directory, icon_filename):
    """ Simple function to load and parse an XML file. """
    icon_path = os.path.join(source_directory, icon_filename)
    xml_tree = ElementTree.parse(icon_path)
    return xml_tree


def xml_svg_write(xml_tree, root_directory, target_icon_filename):
    """ Simple function to write an XML file. """
    icon_path = os.path.join(root_directory, target_icon_filename)
    xml_tree.write(icon_path)


def xml_svg_overlay_parse_groups(xml_root):
    """ Remove sections of an Wine icon (overlay) that are not required. """
    first = True
    for xml_node in xml_root.findall('svg:g', GLOBAL_XMLNS):
        if first:
            first = False
            xml_node.set('transform', 'matrix()')
        else:
            xml_root.remove(xml_node)
    return xml_root


def xml_svg_join_fragmented_groups(xml_root):
    """ Hack to fix XML files with SVG icons that are not combined in a single group. """
    xml_large_icon_node = None
    for xml_node in xml_root.findall('svg:g', GLOBAL_XMLNS):
        if xml_node.attrib.get('id') is None:
            continue
        if xml_large_icon_node is None:
            xml_large_icon_node = copy.deepcopy(xml_node)
            for xml_subnode in xml_large_icon_node.findall('*', GLOBAL_XMLNS):
                xml_large_icon_node.remove(xml_subnode)
            xml_large_icon_node.set('id', '')
            xml_large_icon_node.set('transform', 'translate(0,0)')
        xml_large_icon_node.append(copy.deepcopy(xml_node))
        xml_root.remove(xml_node)
    if xml_large_icon_node is None:
        return xml_root
    xml_root.append(xml_large_icon_node)
    return xml_root


def xml_svg_places_get_transform(icon_size, places_svg_file):
    """ Get transformation matrix for the specified places icon. """
    transformation_data = {}
    if icon_size == GLOBAL_LARGE_SVG_ICON_ID:
        transformation_data['x-scale'] = GLOBAL_OVERLAY_LARGE_X_SCALE
        transformation_data['y-scale'] = GLOBAL_OVERLAY_LARGE_Y_SCALE
        if places_svg_file in ['document.svg', 'desktop.svg', 'mydocs.svg', 'drive.svg',
                               'mycomputer.svg', 'netdrive.svg', 'printer.svg']:
            transformation_data['x'] = '24'
            transformation_data['y'] = '16'
        else:
            transformation_data['x'] = '20'
            transformation_data['y'] = '10'
    elif icon_size == GLOBAL_MEDIUM_SVG_ICON_ID:
        transformation_data['x-scale'] = GLOBAL_OVERLAY_MEDIUM_X_SCALE
        transformation_data['y-scale'] = GLOBAL_OVERLAY_MEDIUM_Y_SCALE
        if places_svg_file in ['desktop.svg', 'mydocs.svg', 'drive.svg',
                               'netdrive.svg', 'printer.svg']:
            transformation_data['x'] = '187'
            transformation_data['y'] = '29'
        elif places_svg_file in ['mycomputer.svg']:
            transformation_data['x'] = '188'
            transformation_data['y'] = '28'
        elif places_svg_file in ['document.svg']:
            transformation_data['x'] = '10'
            transformation_data['y'] = '5'
        else:
            transformation_data['x'] = '13'
            transformation_data['y'] = '7'
    return transformation_data


def xml_do_overlay_svg(xml_base_root, xml_overlay_root, places_svg_file):
    """ Overlay a scaled down XML SVG Wine icon on the specified XML SVG base icon. """
    xml_defs_base = xml_base_root.find('svg:defs', GLOBAL_XMLNS)
    xml_defs_overlay = xml_overlay_root.find('svg:defs', GLOBAL_XMLNS)
    xml_group_overlay = xml_overlay_root.find('svg:g', GLOBAL_XMLNS)
    if xml_defs_base is None or xml_defs_overlay is None or xml_group_overlay is None:
        return xml_base_root
    xml_defs_base.extend(xml_defs_overlay)
    if places_svg_file in ['desktop.svg', 'document.svg', 'mycomputer.svg']:
        icon_order = [GLOBAL_MEDIUM_SVG_ICON_ID, GLOBAL_LARGE_SVG_ICON_ID]
    else:
        icon_order = [GLOBAL_LARGE_SVG_ICON_ID, GLOBAL_MEDIUM_SVG_ICON_ID, GLOBAL_SMALL_SVG_ICON_ID]
    for xml_group_base in xml_base_root.findall('svg:g', GLOBAL_XMLNS):
        if not icon_order:
            break
        xml_group_base.set('id', icon_order[0])
        transformation_matrix = xml_svg_places_get_transform(icon_order[0], places_svg_file)
        icon_order = icon_order[1:]
        if not places_svg_file in ['control.svg']:
            xml_group_overlay_copy = copy.deepcopy(xml_group_overlay)
            xml_group_overlay_copy.set('transform',
                                       'matrix('
                                       +transformation_matrix['x-scale']+',0,0,'
                                       +transformation_matrix['y-scale']+','
                                       +transformation_matrix['x']+','
                                       +transformation_matrix['y']+')')
            xml_group_base.append(xml_group_overlay_copy)
    return xml_base_root


def xml_process_apps_svg_id_element(xml_root, element, max_icon_size):
    """ For the specified application icon embedded PNG icon fix the y coord.
        Remove larger icon references. """
    internal_size = (max_icon_size*3)//4
    icon_border = (max_icon_size-internal_size)//2
    xml_height = int(element.get("height"))
    if element.tag == '{'+GLOBAL_XMLNS['svg']+'}image':
        y_value = max_icon_size-xml_height-icon_border
        element.set('y', str(y_value))
    elif xml_height > max_icon_size:
        xml_root.remove(element)
        element = None
    return xml_root


def xml_process_apps_svg_group(xml_root, element, x_offset, y_offset):
    """ Remove very large application scaled icons (>1x scale) for specified XML element.
        For all other icons set X and Y offsets. """
    xml_transform_attrib = element.attrib.get('transform')
    if xml_transform_attrib is None:
        return xml_root
    matrix_regex = (r'^matrix\('
                    r'([-]*[\.0-9]+)\,'
                    r'([-]*[\.0-9]+)\,'
                    r'([-]*[\.0-9]+)\,'
                    r'([-]*[\.0-9]+)\,'
                    r'([-]*[\.0-9]+)\,'
                    r'([-]*[\.0-9]+)\)$')
    if re.search(matrix_regex, xml_transform_attrib):
        x_scale = re.sub(matrix_regex, r'\1', xml_transform_attrib)
        y_scale = re.sub(matrix_regex, r'\4', xml_transform_attrib)
        x_scale = round(float(x_scale))
        y_scale = round(float(y_scale))
        if x_scale == 1 and y_scale == 1:
            element.set('transform', 'translate()') # dummy translate
        else:
            xml_root.remove(element)
            return xml_root
    if re.search(r'^translate\(.+\)$', xml_transform_attrib):
        element.set('transform', 'translate('+str(x_offset)+', '+str(y_offset)+')')
    return xml_root


def xml_apps_svg_parse_groups(xml_root, apps_svg_file):
    """ Set ID tags for all application SVG scalable icons.
        Set X and Y translation offsets for all application SVG icons
        - to ensure these are 'neatly' lined up. """
    for element in xml_root.findall(".//*[@id]"):
        if re.search(r'^icon\:[0-9]+\-[0-9]+$', element.attrib.get('id')):
            xml_root = xml_process_apps_svg_id_element(xml_root, element, GLOBAL_NEW_ICON_SIZE)
    icon_order = [GLOBAL_LARGE_SVG_ICON_ID, GLOBAL_MEDIUM_SVG_ICON_ID, GLOBAL_SMALL_SVG_ICON_ID]
    if apps_svg_file in ['iexplore.svg', 'notepad.svg']:
        icon_order = [GLOBAL_SMALL_SVG_ICON_ID, GLOBAL_MEDIUM_SVG_ICON_ID, GLOBAL_LARGE_SVG_ICON_ID]
    elif apps_svg_file in ['taskmgr.svg', 'winecfg.svg', 'wordpad.svg']:
        icon_order = [GLOBAL_MEDIUM_SVG_ICON_ID, GLOBAL_LARGE_SVG_ICON_ID]
    first = True
    for element in xml_root.findall(".//svg:g", GLOBAL_XMLNS):
        x_offset = y_offset = 0
        if icon_order:
            element.set('id', icon_order[0])
            icon_order = icon_order[1:]
        if int(xml_root.get('height')) <= GLOBAL_NEW_ICON_SIZE:
            continue
        if first:
            first = False
            if apps_svg_file in ['taskmgr.svg', 'wcmd.svg', 'winefile.svg',
                                 'winhelp.svg', 'winemine.svg']:
                x_offset = y_offset = 8
            elif apps_svg_file in ['winecfg.svg']:
                x_offset = 176
                y_offset = 24
        if element.get('transform') != None:
            xml_root = xml_process_apps_svg_group(xml_root, element, x_offset, y_offset)
    return xml_root


def xml_svg_fix_icon_size(xml_root):
    """ Set main XML SVG icon size and use employ a hack to set a newer version of Inkscape. """
    xml_root.set('{'+GLOBAL_XMLNS['inkscape']+'}version', str(GLOBAL_NEW_INKSCAPE_VERSION))
    xml_root.set('height', str(GLOBAL_NEW_ICON_SIZE))
    xml_root.set('width', str(GLOBAL_NEW_ICON_SIZE))
    return xml_root


def process_wine_icon(wine_source_directory, target_root_directory):
    """ Clone wine (Windows) icon file. """
    print(f'{GLOBAL_WINE_ICON_LOGO_FILENAME} ', end='')
    source_path = os.path.join(wine_source_directory, GLOBAL_WINE_LOGO_DIRECTORY)
    source_path = os.path.join(source_path, GLOBAL_WINE_ICON_LOGO_FILENAME)
    destination_path = os.path.join(target_root_directory, GLOBAL_ICONS_TARGET_RELPATH)
    destination_path = os.path.join(destination_path, GLOBAL_WINE_ICON_LOGO_FILENAME)
    shutil.copyfile(source_path, destination_path)


def process_apps_svg_files(wine_source_directory, target_root_directory):
    """ Loop through and process all application icons
        - cloning these from the specified Wine Source tree. """
    for apps_svg_file in GLOBAL_APP_SVG_FILES:
        print(f'{apps_svg_file} ', end='')
        sys.stdout.flush()
        source_rel_directory = GLOBAL_APP_SVG_FILES[apps_svg_file]['srpath']
        source_directory = os.path.join(wine_source_directory, source_rel_directory)
        target_rel_path = GLOBAL_APP_SVG_FILES[apps_svg_file]['trpath']
        target_directory = os.path.join(target_root_directory, target_rel_path)
        xml_tree = xml_svg_load_and_parse(source_directory, apps_svg_file)
        xml_root = xml_tree.getroot()
        xml_root = xml_apps_svg_parse_groups(xml_root, apps_svg_file)
        xml_root = xml_svg_fix_icon_size(xml_root)
        if apps_svg_file == GLOBAL_WINE_SVG_LOGO_FILENAME:
            apps_svg_file = 'wine.svg'
        else:
            apps_svg_file = 'wine-'+apps_svg_file
        xml_svg_write(xml_tree, target_directory, apps_svg_file)


def process_places_svg_files(wine_source_directory, target_root_directory):
    """ Loop through and process all places icons
        - cloning these from the specified Wine Source tree. """
    source_directory = os.path.join(wine_source_directory, GLOBAL_WINE_LOGO_DIRECTORY)
    xml_overlay_tree = xml_svg_load_and_parse(source_directory, GLOBAL_WINE_SVG_LOGO_FILENAME)
    xml_overlay_root = xml_overlay_tree.getroot()
    xml_overlay_root = xml_svg_overlay_parse_groups(xml_overlay_root)
    for places_svg_file in GLOBAL_PLACES_SVG_FILES:
        print(f'{places_svg_file} ', end='')
        sys.stdout.flush()
        source_rel_directory = GLOBAL_PLACES_SVG_FILES[places_svg_file]['srpath']
        source_directory = os.path.join(wine_source_directory, source_rel_directory)
        target_rel_path = GLOBAL_PLACES_SVG_FILES[places_svg_file]['trpath']
        target_directory = os.path.join(target_root_directory, target_rel_path)
        xml_tree = xml_svg_load_and_parse(source_directory, places_svg_file)
        xml_root = xml_tree.getroot()
        if places_svg_file == 'document.svg':
            xml_root = xml_svg_join_fragmented_groups(xml_root)
        xml_root = xml_do_overlay_svg(xml_root, xml_overlay_root, places_svg_file)
        xml_root = xml_svg_fix_icon_size(xml_root)
        places_svg_file = re.sub(r'(\.svg)', r'-wine\1', places_svg_file)
        xml_svg_write(xml_tree, target_directory, places_svg_file)


def create_makefile_variable(root_directory, subdirectory, variable_name, file_type):
    """ Create a single variable for Makefile. """
    search_directory = os.path.join(root_directory, subdirectory)
    if not os.path.exists(search_directory):
        os.makedirs(search_directory)
    source_files = []
    with os.scandir(search_directory) as it_directory:
        for directory_entry in it_directory:
            if (not directory_entry.name.startswith('.') and
                    directory_entry.is_file() and
                    directory_entry.name.endswith("."+file_type)
               ):
                path = os.path.join(search_directory, directory_entry)
                path = os.path.relpath(path, root_directory)
                source_files.append(path)
    if len(source_files) == 1:
        file_text = variable_name+" = "+source_files[0]
    elif len(source_files) > 1:
        source_files.sort()
        file_text = variable_name+"  = "
        for source_file in source_files:
            file_text += " \\\n\t"+source_file
    else:
        file_text = ""
    if len(source_files) >= 1:
        file_text += "\n\n"
    return file_text


def create_makefile(root_directory):
    """ Generate Makefile - referencing all file_types which are to be installed """
    file_installation_list = \
        [('MENU_FILES',
          'menu',
          'xdg/',
          '/etc/xdg/menus/applications-merged'),
         ('DESKTOP_FILES',
          'desktop',
          'applications/',
          '/usr/share/applications'),
         ('DIRECTORY_FILES',
          'directory',
          'desktop-directories/',
          '/usr/share/desktop-directories'),
         ('APPS_ICONS',
          'svg',
          GLOBAL_SVG_APPS_TARGET_RELPATH,
          '/usr/share/icons/hicolor/scalable/apps'),
         ('PLACES_ICONS',
          'svg',
          GLOBAL_SVG_PLACES_TARGET_RELPATH,
          '/usr/share/icons/hicolor/scalable/places'),
         ('WINE_ICO',
          'ico',
          GLOBAL_ICONS_TARGET_RELPATH,
          '/usr/share/wine/icons')]
    file_text = ""
    for file_type_tuple in file_installation_list:
        file_text += create_makefile_variable(root_directory,
                                              file_type_tuple[2],
                                              file_type_tuple[0],
                                              file_type_tuple[1]
                                             )
    file_text += 'all:'
    for file_type_tuple in file_installation_list:
        file_text += ' $('+file_type_tuple[0]+')'
    file_text += '\n\ninstall: all\n'
    for file_type_tuple in file_installation_list:
        file_text += ('\tinstall -d "$(DESTDIR)$(EPREFIX)'
                      +file_type_tuple[3]
                      +'"\n')
        file_text += ('\tinstall -m0644 $('
                      +file_type_tuple[0]
                      +') "$(DESTDIR)$(EPREFIX)'
                      +file_type_tuple[3]
                      +'"\n')
    if not os.path.exists(root_directory):
        os.makedirs(root_directory)
    path = os.path.join(root_directory, "Makefile")
    with open(path, "w") as file_handle:
        file_handle.write(file_text)


def main():
    """ Module to generate Distribution Agnostic Wine icon, .desktop and .menu data files. """
    parser = argparse.ArgumentParser(description=('Python script to generate Wine .svg/.ico icon,'
                                                  '.desktop and .menu data files.'),
                                     usage='%(prog)s [options]')
    parser.add_argument('-t', '--target', nargs='?', default=os.getcwd(),
                        help='Root directory target for building')
    parser.add_argument('-w', '--wine', nargs='?',
                        help='Wine Source directory')
    args = parser.parse_args()
    target_directory = args.target
    target_directory = os.path.realpath(target_directory)
    if not os.path.isdir(target_directory):
        parser.print_help()
        print(f'\nTarget: {target_directory} is not a valid, pre-existing directory')
        exit(1)
    wine_source_directory = args.wine
    if wine_source_directory is None:
        parser.print_help()
        print(f'\nWine Source directory not specified')
        exit(2)
    wine_source_directory = os.path.realpath(wine_source_directory)
    if not os.path.isdir(wine_source_directory):
        parser.print_help()
        print(f'\nWine Source directory: '
              +wine_source_directory
              +' is not a valid, pre-existing directory')
        exit(2)
    print('Clean all subdirectories and files...')
    clean_all(target_directory)
    print('Create all subdirectories...')
    create_subdirectories(target_directory)
    print('Clone and modify Wine icons... ', end='')
    xml_register_svg_ns()
    process_wine_icon(wine_source_directory, target_directory)
    process_apps_svg_files(wine_source_directory, target_directory)
    process_places_svg_files(wine_source_directory, target_directory)
    print('\nCreate Wine Desktop files... ', end='')
    sys.stdout.flush()
    create_wine_desktop_files(os.path.join(target_directory, "applications"))
    print('\nCreate Wine XDG Menu file...')
    create_menu_file(os.path.join(target_directory, "xdg"))
    print('Create Wine Menu files... ', end='')
    sys.stdout.flush()
    create_wine_menu_files(os.path.join(target_directory, "desktop-directories"))
    print('\nCreate Makefile...')
    create_makefile(target_directory)

if __name__ == '__main__':
    main()
