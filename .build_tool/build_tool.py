#!/usr/bin/env python3.6

""" Module to generate Linux Distribution Agnostic Wine icon, .desktop and .menu data files. """

import argparse
import copy
import os
import re
import shutil
import string
import subprocess
import sys
import xml.etree.ElementTree as ElementTree
import global_variables

def clean_all(root_directory):
    """ Remove all directories and main Makefile """
    if os.path.exists(root_directory) and os.path.isdir(root_directory):
        for directory in global_variables.SUBDIRECTORIES:
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
    sudirectory_list = global_variables.SUBDIRECTORIES
    sudirectory_list += [global_variables.SVG_APPS_TARGET_RELPATH,
                         global_variables.SVG_PLACES_TARGET_RELPATH]
    for subdirectory in sudirectory_list:
        create_subdirectory(root_directory, subdirectory)


def mangle_protected_term(protected_term):
    """ Mangle a protected technical term - to ensure it is note
    subject to translation. """
    mangled_protected_term = ''.join(filter(lambda x:
                                            x in string.ascii_uppercase, protected_term.upper()))
    return mangled_protected_term


def remove_invalid_translations(translated_text_list):
    """ Remove translations from a translation list that contain
    mangled CRC codes. """
    protected_ids = []
    for protected_term in global_variables.PROTECTED_TERMS_DICT:
        protected_ids += [global_variables.PROTECTED_TERMS_DICT[protected_term]]
    valid_translated_text_list = []
    for translated_text in translated_text_list:
        if translated_text == '':
            continue
        valid = True
        for match in re.findall(r'[0-9]{10,}', translated_text):
            if not match in protected_ids:
                valid = False
                break
        if valid:
            valid_translated_text_list += [translated_text]
    return valid_translated_text_list


def find_best_translation(untranslated_text, translated_text_list):
    """ Accepts a base (English) language string and a source list of translation strings.
    Filters the list of translated strings returning the one with the least matches
    against any words from the base (English) language string."""
    untranslated_word_list = re.split(' ', untranslated_text)
    untranslated_word_count = len(untranslated_word_list)
    current_score = len(untranslated_text)
    target_text = ""
    mangled_protected_terms_list = [global_variables.PROTECTED_TERMS_DICT[x]
                                    for x in global_variables.PROTECTED_TERMS_DICT]
    for translated_text in translated_text_list:
        translated_text = translated_text.strip()
        translated_text = translated_text.replace('\"', '')
        if re.search(r'^[0-9]{10,}$', translated_text) and untranslated_word_count > 1:
            continue
        translated_word_list = re.split(' ', translated_text)
        translated_word_count = len(translated_word_list)
        score = 0
        if translated_text.upper() == untranslated_text.upper():
            score = untranslated_word_count
        score += abs(translated_word_count - untranslated_word_count)
        for untranslated_word in untranslated_word_list:
            offset = len(untranslated_word)
            if (untranslated_word.upper() in mangled_protected_terms_list
                    and untranslated_word_count > 1):
                offset = -offset
            if untranslated_word.upper() in translated_text.upper():
                score += offset
        if score < current_score or target_text == "":
            target_text = translated_text
            current_score = score
    return target_text


def do_translate_text(text, locale):
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
    translation_list = re.split(r'\n|\,|^\(|\)$', out.stdout, flags=re.MULTILINE)
    translation_list = remove_invalid_translations(translation_list)
    translated_text = find_best_translation(text, translation_list)
    return translated_text


def pre_translate_terms():
    """ Translate a list of non-technical terms that are safe to translate,
    without affecting their meaning."""
    for locale in global_variables.TRANSLATION_DICTIONARY:
        if locale == "en":
            continue
        locale_dictionary = global_variables.TRANSLATION_DICTIONARY[locale]
        for unprotected_term in global_variables.UNPROTECTED_TERMS:
            if unprotected_term in locale_dictionary:
                continue
            locale_dictionary[unprotected_term] = do_translate_text(unprotected_term, locale)
        for protected_term in global_variables.PROTECTED_TERMS_DICT:
            if protected_term in locale_dictionary:
                continue
            if re.search(r'^[A-Z]:$', protected_term):
                locale_dictionary[protected_term] = protected_term
            else:
                locale_dictionary[protected_term] = do_translate_text(protected_term, locale)


def translate_text(text, locale):
    """ Carry out the translation of a non-english phrase. """
    # Protect technical terms, we do not want to be translated ...
    locale_dictionary = global_variables.TRANSLATION_DICTIONARY[locale]
    protected_term_list = []
    translated_text = do_translate_text(text, locale)
    for protected_term in global_variables.PROTECTED_TERMS_DICT:
        new_text = text.replace(protected_term,
                                global_variables.PROTECTED_TERMS_DICT[protected_term])
        if new_text != text:
            text = new_text
            protected_term_list += [protected_term]
    if not protected_term_list:
        protected_translated_text = translated_text
    else:
        protected_translated_text = do_translate_text(text, locale)
    for unprotected_term in global_variables.UNPROTECTED_TERMS:
        if unprotected_term in locale_dictionary:
            translated_text = \
                    translated_text.replace(unprotected_term,
                                            locale_dictionary[unprotected_term])
            protected_translated_text = \
                    protected_translated_text.replace(unprotected_term,
                                                      locale_dictionary[unprotected_term])
    # ... then convert these terms back.
    translation_ok = True
    for protected_term in protected_term_list:
        protected_translated_text = \
            protected_translated_text.replace(global_variables.PROTECTED_TERMS_DICT[protected_term],
                                              protected_term)
        if not translation_ok:
            continue
        new_translated_text = translated_text.replace(locale_dictionary[protected_term],
                                                      protected_term)
        if new_translated_text == translated_text:
            new_translated_text = translated_text.replace(locale_dictionary[protected_term].lower(),
                                                          protected_term)
        if new_translated_text != translated_text:
            translated_text = new_translated_text
        else:
            translation_ok = False
    if translation_ok:
        return translated_text
    return protected_translated_text


def translate_text_lookup(text, locale):
    """ Translate a phrase or word and return result.
        Use a dictionary so subsequent lookups are faster."""
    locale_dictionary = global_variables.TRANSLATION_DICTIONARY[locale]
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
    for locale in global_variables.TRANSLATION_DICTIONARY:
        if locale == "en":
            file_text += f'{entry}={content}\n'
        else:
            translated_text = translate_text_lookup(content, locale)
            file_text += f'{entry}[{locale}]={translated_text}\n'
    return file_text


def create_xdg_type_entry(file_content):
    """ Generate a XDG file type entry.
        Also create exec and terminal entries if specified, if is application. """
    file_text = ""
    if file_content["Type"] == "Application":
        # Exec
        if "Exec" in file_content:
            file_text += f'Exec={file_content["Exec"]}\n'
        # Terminal
        if "Terminal" in file_content:
            file_text += f'Terminal={file_content["Terminal"]}\n'
    # Type
    file_text += f'Type={file_content["Type"]}\n'
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
        file_text += f'Icon={file_content["Icon"]}\n'
    # MimeType
    if "MimeType" in file_content:
        mime_types = ""
        for mime_type in file_content["MimeType"]:
            mime_types += mime_type+";"
        file_text += f'MimeType={mime_types}\n'
    # Hidden
    if "Hidden" in file_content and file_content["Hidden"]:
        file_text += f'Hidden={file_content["Hidden"]}\n'
    # NoDisplay
    if "NoDisplay" in file_content and file_content["NoDisplay"]:
        file_text += f'NoDisplay={file_content["NoDisplay"]}\n'
    # Categories
    if "Categories" in file_content:
        categories = ""
        for category in file_content["Categories"]:
            categories += category+";"
        file_text += f'Categories={categories}\n'
    if "StartupWMClass" in file_content:
        file_text += f'StartupWMClass={file_content["StartupWMClass"]}\n'
    with open(path, "w") as file_handle:
        file_handle.write(file_text)

def create_wine_desktop_files(directory):
    """ Create all Wine .desktop launcher files. """
    if not os.path.exists(directory):
        os.makedirs(directory)
    for desktop_file in global_variables.DESKTOP_FILE_DICT:
        path = os.path.join(directory, desktop_file+".desktop")
        create_xdg_file(path, global_variables.DESKTOP_FILE_DICT[desktop_file])


def create_menu_file(directory, prefix):
    """ Generate a menu global file, which references custom Wine application Categories """
    def generate_menu_entry(indent, i, names):
        """ Helper to add a nested menu entry to menu file """
        file_text = indent*i+"<Menu>\n"
        name = re.sub(r'^Wine', r'wine', names[0])
        name = re.sub(r'^wine\-', r'', name)
        file_text += indent*(i+1)+"<Name>"+prefix+global_variables.VENDOR_ID+"-"+name+"</Name>\n"
        directory = prefix.lower()+global_variables.VENDOR_ID+"-"+name+".directory"
        file_text += indent*(i+1)+"<Directory>"+directory+"</Directory>\n"
        file_text += indent*(i+1)+"<Include>\n"
        file_text += indent*(i+2)+"<Category>"+prefix+names[0]+"</Category>\n"
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
    file_text += ' "http://www.freedesktop.org/standards/menu-spec/menu-1.0.dtd">\n'
    file_text += '<Menu>\n'+indent+'<Name>'+entry_type+'</Name>\n'
    file_text += generate_menu_entry(indent, i, global_variables.WINE_DESKTOP_FILES)
    file_text += "</Menu>\n"
    path = prefix.lower()+global_variables.VENDOR_ID+".menu"
    print(f'{path} ', end='')
    path = os.path.join(directory, path)
    with open(path, "w") as file_handle:
        file_handle.write(file_text)


def create_wine_menu_files(directory, prefix):
    """ Create Wine menu files """
    entry_type = "Directory"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for desktop_file in global_variables.WINE_DESKTOP_FILES:
        desktop_filename = re.sub(r'^Wine', r'wine', desktop_file)
        desktop_filename = re.sub(r'^wine\-', r'', desktop_filename)
        desktop_filename = (prefix.lower()+global_variables.VENDOR_ID
                            +"-"+desktop_filename+".directory")
        path = os.path.join(directory, desktop_filename)
        icon = 'folder'
        name = re.sub(r'.*\-', r'', desktop_file)
        if desktop_file == "Wine":
            icon = 'wine'
            name = prefix+name
        desktop_file_contents = {"Name":name, "Type":entry_type, "Icon":icon}
        create_xdg_file(path, desktop_file_contents)


def xml_register_svg_ns():
    """ Register all global SVG XML namespaces wtth ElementTree module. """
    for name_space in global_variables.XMLNS:
        ElementTree.register_namespace(name_space, global_variables.XMLNS[name_space])
        if name_space == 'svg':
            ElementTree.register_namespace('', global_variables.XMLNS[name_space])


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
    for xml_node in xml_root.findall('svg:g', global_variables.XMLNS):
        if first:
            first = False
            xml_node.set('transform', 'matrix()')
        else:
            xml_root.remove(xml_node)
    return xml_root


def xml_svg_join_fragmented_groups(xml_root):
    """ Hack to fix XML files with SVG icons that are not combined in a single group. """
    xml_large_icon_node = None
    for xml_node in xml_root.findall('svg:g', global_variables.XMLNS):
        if xml_node.attrib.get('id') is None:
            continue
        if xml_large_icon_node is None:
            xml_large_icon_node = copy.deepcopy(xml_node)
            for xml_subnode in xml_large_icon_node.findall('*', global_variables.XMLNS):
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
    if icon_size == global_variables.LARGE_SVG_ICON_ID:
        transformation_data['x-scale'] = global_variables.OVERLAY_LARGE_X_SCALE
        transformation_data['y-scale'] = global_variables.OVERLAY_LARGE_Y_SCALE
        if places_svg_file in ['document.svg', 'desktop.svg', 'mydocs.svg', 'drive.svg',
                               'mycomputer.svg', 'netdrive.svg', 'printer.svg']:
            transformation_data['x'] = '24'
            transformation_data['y'] = '16'
        else:
            transformation_data['x'] = '20'
            transformation_data['y'] = '10'
    elif icon_size == global_variables.MEDIUM_SVG_ICON_ID:
        transformation_data['x-scale'] = global_variables.OVERLAY_MEDIUM_X_SCALE
        transformation_data['y-scale'] = global_variables.OVERLAY_MEDIUM_Y_SCALE
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
    xml_defs_base = xml_base_root.find('svg:defs', global_variables.XMLNS)
    xml_defs_overlay = xml_overlay_root.find('svg:defs', global_variables.XMLNS)
    xml_group_overlay = xml_overlay_root.find('svg:g', global_variables.XMLNS)
    if xml_defs_base is None or xml_defs_overlay is None or xml_group_overlay is None:
        return xml_base_root
    xml_defs_base.extend(xml_defs_overlay)
    if places_svg_file in ['desktop.svg', 'document.svg', 'mycomputer.svg']:
        icon_order = [global_variables.MEDIUM_SVG_ICON_ID,
                      global_variables.LARGE_SVG_ICON_ID]
    else:
        icon_order = [global_variables.LARGE_SVG_ICON_ID,
                      global_variables.MEDIUM_SVG_ICON_ID,
                      global_variables.SMALL_SVG_ICON_ID]
    for xml_group_base in xml_base_root.findall('svg:g', global_variables.XMLNS):
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
    if element.tag == '{'+global_variables.XMLNS['svg']+'}image':
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
            xml_root = xml_process_apps_svg_id_element(xml_root,
                                                       element,
                                                       global_variables.NEW_ICON_SIZE)
    icon_order = [global_variables.LARGE_SVG_ICON_ID,
                  global_variables.MEDIUM_SVG_ICON_ID,
                  global_variables.SMALL_SVG_ICON_ID]
    if apps_svg_file in ['iexplore.svg', 'notepad.svg']:
        icon_order = [global_variables.SMALL_SVG_ICON_ID,
                      global_variables.MEDIUM_SVG_ICON_ID,
                      global_variables.LARGE_SVG_ICON_ID]
    elif apps_svg_file in ['taskmgr.svg', 'winecfg.svg', 'wordpad.svg']:
        icon_order = [global_variables.MEDIUM_SVG_ICON_ID,
                      global_variables.LARGE_SVG_ICON_ID]
    first = True
    for element in xml_root.findall(".//svg:g", global_variables.XMLNS):
        x_offset = y_offset = 0
        if icon_order:
            element.set('id', icon_order[0])
            icon_order = icon_order[1:]
        if int(xml_root.get('height')) <= global_variables.NEW_ICON_SIZE:
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
    xml_root.set('{'+global_variables.XMLNS['inkscape']+'}version',
                 str(global_variables.NEW_INKSCAPE_VERSION))
    xml_root.set('height', str(global_variables.NEW_ICON_SIZE))
    xml_root.set('width', str(global_variables.NEW_ICON_SIZE))
    return xml_root


def process_wine_icon(wine_source_directory, target_root_directory):
    """ Clone wine (Windows) icon file. """
    print(f'{global_variables.WINE_ICON_LOGO_FILENAME} ', end='')
    source_path = os.path.join(wine_source_directory, global_variables.WINE_LOGO_DIRECTORY)
    source_path = os.path.join(source_path, global_variables.WINE_ICON_LOGO_FILENAME)
    destination_path = os.path.join(target_root_directory, global_variables.ICONS_TARGET_RELPATH)
    destination_path = os.path.join(destination_path, global_variables.WINE_ICON_LOGO_FILENAME)
    shutil.copyfile(source_path, destination_path)


def process_apps_svg_files(wine_source_directory, target_root_directory):
    """ Loop through and process all application icons
        - cloning these from the specified Wine Source tree. """
    for apps_svg_file in global_variables.APP_SVG_FILES:
        print(f'{apps_svg_file} ', end='')
        sys.stdout.flush()
        source_rel_directory = global_variables.APP_SVG_FILES[apps_svg_file]['srpath']
        source_directory = os.path.join(wine_source_directory, source_rel_directory)
        target_rel_path = global_variables.APP_SVG_FILES[apps_svg_file]['trpath']
        target_directory = os.path.join(target_root_directory, target_rel_path)
        xml_tree = xml_svg_load_and_parse(source_directory, apps_svg_file)
        xml_root = xml_tree.getroot()
        xml_root = xml_apps_svg_parse_groups(xml_root, apps_svg_file)
        xml_root = xml_svg_fix_icon_size(xml_root)
        if apps_svg_file == global_variables.WINE_SVG_LOGO_FILENAME:
            apps_svg_file = 'wine.svg'
        else:
            apps_svg_file = 'wine-'+apps_svg_file
        xml_svg_write(xml_tree, target_directory, apps_svg_file)


def process_places_svg_files(wine_source_directory, target_root_directory):
    """ Loop through and process all places icons
        - cloning these from the specified Wine Source tree. """
    source_directory = os.path.join(wine_source_directory, global_variables.WINE_LOGO_DIRECTORY)
    xml_overlay_tree = xml_svg_load_and_parse(source_directory,
                                              global_variables.WINE_SVG_LOGO_FILENAME)
    xml_overlay_root = xml_overlay_tree.getroot()
    xml_overlay_root = xml_svg_overlay_parse_groups(xml_overlay_root)
    for places_svg_file in global_variables.PLACES_SVG_FILES:
        print(f'{places_svg_file} ', end='')
        sys.stdout.flush()
        source_rel_directory = global_variables.PLACES_SVG_FILES[places_svg_file]['srpath']
        source_directory = os.path.join(wine_source_directory, source_rel_directory)
        target_rel_path = global_variables.PLACES_SVG_FILES[places_svg_file]['trpath']
        target_directory = os.path.join(target_root_directory, target_rel_path)
        xml_tree = xml_svg_load_and_parse(source_directory, places_svg_file)
        xml_root = xml_tree.getroot()
        if places_svg_file == 'document.svg':
            xml_root = xml_svg_join_fragmented_groups(xml_root)
        xml_root = xml_do_overlay_svg(xml_root, xml_overlay_root, places_svg_file)
        xml_root = xml_svg_fix_icon_size(xml_root)
        places_svg_file = global_variables.VENDOR_ID+'-'+places_svg_file
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
          global_variables.SVG_APPS_TARGET_RELPATH,
          '/usr/share/icons/hicolor/scalable/apps'),
         ('PLACES_ICONS',
          'svg',
          global_variables.SVG_PLACES_TARGET_RELPATH,
          '/usr/share/icons/hicolor/scalable/places'),
         ('WINE_ICO',
          'ico',
          global_variables.ICONS_TARGET_RELPATH,
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
    global_variables.init()
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
    print('Pre-translate (non-)technical, (un)protected terms...')
    pre_translate_terms()
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
    print('\nCreate Wine XDG Menu files...', end='')
    sys.stdout.flush()
    create_menu_file(os.path.join(target_directory, "xdg"), "")
    print('\nCreate Wine Menu files... ', end='')
    sys.stdout.flush()
    create_wine_menu_files(os.path.join(target_directory, "desktop-directories"), "")
    print('\nCreate Makefile...')
    create_makefile(target_directory)

if __name__ == '__main__':
    main()
