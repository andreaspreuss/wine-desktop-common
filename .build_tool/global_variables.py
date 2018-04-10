#!/usr/bin/env python3.6

""" Global variables for build_tool.py script """

import os

VENDOR_ID = None
TRANSLATION_DICTIONARY = None
PROTECTED_TERMS_DICT = None
UNPROTECTED_TERMS = None
WINE_CATEGORIES = None
GENERAL_CATEGORIES = None
TYPE = None
DESKTOP_FILE_DICT = None
WINE_DESKTOP_FILES = None
NEW_INKSCAPE_VERSION = None
NEW_ICON_SIZE = None
ICONS_TARGET_RELPATH = None
SVG_TARGET_RELPATH = None
OVERLAY_LARGE_X_SCALE = None
OVERLAY_LARGE_Y_SCALE = None
OVERLAY_MEDIUM_X_SCALE = None
OVERLAY_MEDIUM_Y_SCALE = None
WINE_LOGO_DIRECTORY = None
WINE_SVG_LOGO_FILENAME = None
WINE_ICON_LOGO_FILENAME = None
SVG_APPS_TARGET_RELPATH = None
APP_SVG_FILES = None
SVG_PLACES_TARGET_RELPATH = None
PLACES_SVG_FILES = None
LARGE_SVG_ICON_ID = None
MEDIUM_SVG_ICON_ID = None
SMALL_SVG_ICON_ID = None
XMLNS = None
SUBDIRECTORIES = None


def init():
    """ Define all global variables for build_tool.py script """
    # pylint: disable=global-statement
    # pylint: disable=too-many-statements
    global VENDOR_ID
    global TRANSLATION_DICTIONARY
    global PROTECTED_TERMS_DICT
    global UNPROTECTED_TERMS
    global WINE_CATEGORIES
    global GENERAL_CATEGORIES
    global TYPE
    global DESKTOP_FILE_DICT
    global WINE_DESKTOP_FILES
    global NEW_INKSCAPE_VERSION
    global NEW_ICON_SIZE
    global ICONS_TARGET_RELPATH
    global SVG_TARGET_RELPATH
    global OVERLAY_LARGE_X_SCALE
    global OVERLAY_LARGE_Y_SCALE
    global OVERLAY_MEDIUM_X_SCALE
    global OVERLAY_MEDIUM_Y_SCALE
    global WINE_LOGO_DIRECTORY
    global WINE_SVG_LOGO_FILENAME
    global WINE_ICON_LOGO_FILENAME
    global SVG_APPS_TARGET_RELPATH
    global APP_SVG_FILES
    global SVG_PLACES_TARGET_RELPATH
    global PLACES_SVG_FILES
    global LARGE_SVG_ICON_ID
    global MEDIUM_SVG_ICON_ID
    global SMALL_SVG_ICON_ID
    global XMLNS
    global SUBDIRECTORIES
    VENDOR_ID = 'wine'
    TRANSLATION_DICTIONARY = {"en":{},
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
    # Protect these technical/company terms from translation
    # - replace them temporarily, during translation, with a CRC checksum.
    PROTECTED_TERMS_DICT = {'C:':'001116292070',
                            'Microsoft®':'002181990571',
                            'Windows':'001391736148',
                            'Wine':'002712425879'}
    UNPROTECTED_TERMS = ['Component', 'Editor', 'Object', 'Model', 'Text', 'Viewer']

    # Categories
    WINE_CATEGORIES = {"wine":"Wine",
                       "programs":"Wine-Programs",
                       "accessories":"Wine-Programs-Accessories"}
    GENERAL_CATEGORIES = {"game":"Game", "logic-game":"LogicGame"}

    # Desktop launcher files
    TYPE = "Application"
    DESKTOP_FILE_DICT = {
        VENDOR_ID+"browsecdrive":{"Name":'Wine C: disk-drive',
                                  "Comment":'Browse your virtual C: disk-drive',
                                  "Exec":'sh -c "xdg-open $(winepath -u \'C:\' 2>/dev/null)"',
                                  "Icon":'drive-wine',
                                  "Terminal":"false",
                                  "Type":TYPE,
                                  "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"cmd":{"Name":'Wine Command interpreter',
                         "Comment":'Starts a new instance of the command interpreter CMD',
                         "Type":TYPE,
                         "Exec":'wine cmd.exe',
                         "Icon":'wine-wcmd',
                         "Hidden":'true',
                         "StartupWMClass":'cmd.exe',
                         "Categories":[WINE_CATEGORIES["wine"],
                                       WINE_CATEGORIES["accessories"]]},
        VENDOR_ID+"control":{"Name":'Wine Control',
                             "Comment":'A clone of the Microsoft® Windows Control Panel',
                             "Type":TYPE,
                             "Exec":'wine control.exe',
                             "Icon":'control-wine',
                             "Terminal":'false',
                             "StartupWMClass":'control.exe',
                             "Categories":[WINE_CATEGORIES["wine"],
                                           WINE_CATEGORIES["accessories"]]},
        VENDOR_ID+"explorer":{"Name":'Wine Explorer',
                              "Comment":'A clone of Microsoft® Windows Explorer',
                              "Type":TYPE,
                              "Exec":'wine explorer.exe',
                              "Icon":'wine-winefile',
                              "Terminal":'false',
                              "StartupWMClass":'explorer.exe',
                              "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"iexplore":{"Name":'Wine Internet Explorer',
                              "Comment":('Builtin clone of '
                                         'Microsoft® Windows Internet Explorer®'),
                              "Type":TYPE,
                              "Exec":'wine iexplore.exe %U',
                              "Icon":'wine-iexplore',
                              "Terminal":'false',
                              "StartupWMClass":'iexplore.exe',
                              "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"notepad":{"Name":'Wine Notepad',
                             "Comment":'A clone of the Microsoft® Windows Notepad Text Editor',
                             "Type":TYPE,
                             "Exec":'notepad %f',
                             "Icon":'wine-notepad',
                             "Terminal":'false',
                             "StartupWMClass":'notepad.exe',
                             "Categories":[WINE_CATEGORIES["wine"],
                                           WINE_CATEGORIES["accessories"]]},
        VENDOR_ID+"oleview":{"Name":'Wine OLE/COM Object Viewer',
                             "Comment":('Microsoft® Windows Object Linking and '
                                        'Embedding/Component Object Model Object Viewer'),
                             "Type":TYPE,
                             "Exec":'wine oleview.exe',
                             "Icon":'control-wine',
                             "Terminal":'false',
                             "StartupWMClass":'oleview.exe',
                             "Categories":[WINE_CATEGORIES["wine"],
                                           WINE_CATEGORIES["accessories"]]},
        VENDOR_ID+"regedit":{"Name":'Wine Registry Editor',
                             "Comment":'A clone of the Microsoft® Windows Registry Editor',
                             "Type":TYPE,
                             "Exec":'regedit',
                             "Icon":'wine-regedit',
                             "Terminal":'false',
                             "StartupWMClass":'regedit.exe',
                             "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"taskmgr":{"Name":'Wine Task Manager',
                             "Comment":'A clone of the Microsoft® Windows Task Manager',
                             "Type":TYPE,
                             "Exec":'wine taskmgr.exe',
                             "Icon":'wine-taskmgr',
                             "Terminal":'false',
                             "StartupWMClass":'taskmgr.exe',
                             "Categories":[WINE_CATEGORIES["wine"],
                                           WINE_CATEGORIES["accessories"]]},
        VENDOR_ID+"uninstaller":{"Name":'Wine Software uninstaller',
                                 "Comment":('A clone of the Microsoft® Windows '
                                            'Add and Remove Programs Utility'),
                                 "Type":TYPE,
                                 "Exec":'wine uninstaller.exe',
                                 "Icon":'control-wine',
                                 "Terminal":'false',
                                 "StartupWMClass":'uninstaller.exe',
                                 "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"boot":{"Name":'Wine System-Boot',
                          "Comment":'Simulate System-reboot / System-halt',
                          "Type":TYPE,
                          "Exec":'wineboot',
                          "Icon":'mycomputer-wine',
                          "Terminal":'false',
                          "StartupWMClass":'wineboot.exe',
                          "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"cfg":{"Name":'Wine Configuration',
                         "Comment":('Change general Wine options '
                                    'and application overrides/options'),
                         "Type":TYPE,
                         "Exec":'winecfg',
                         "Icon":'wine-winecfg',
                         "Terminal":'false',
                         "StartupWMClass":'winecfg.exe',
                         "Categories":[WINE_CATEGORIES["wine"],
                                       WINE_CATEGORIES["accessories"]]},
        VENDOR_ID+"file":{"Name":'Wine File Browser',
                          "Comment":'A clone of Microsoft® Windows Explorer',
                          "Type":TYPE,
                          "Exec":'winefile',
                          "Icon":'wine-winefile',
                          "StartupWMClass":'winefile.exe',
                          "Terminal":'false',
                          "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"mine":{"Name":'Wine Minesweeper',
                          "Comment":'A clone of the Microsoft® Windows Minesweeper game',
                          "Type":TYPE,
                          "Exec":'winemine',
                          "Icon":'wine-winemine',
                          "Terminal":'false',
                          "StartupWMClass":'winemine.exe',
                          "Categories":[WINE_CATEGORIES["wine"],
                                        GENERAL_CATEGORIES["game"],
                                        GENERAL_CATEGORIES["logic-game"]]},
        VENDOR_ID+"winhelp":{"Name":'Wine Help',
                             "Comment":'A clone of the Microsoft® Windows Help File browser',
                             "Type":TYPE,
                             "Exec":'wine winhlp32.exe %f',
                             "Icon":'wine-winhelp',
                             "Terminal":'false',
                             "StartupWMClass":'winhlp32.exe',
                             "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"wordpad":{"Name":'Wine Wordpad',
                             "Comment":'A clone of the Microsoft® Windows Wordpad Text Editor',
                             "Type":TYPE,
                             "Exec":'wine wordpad %f',
                             "Icon":'wine-wordpad',
                             "Terminal":'false',
                             "StartupWMClass":'wordpad.exe',
                             "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"msiexec":{"Name":'Wine clone of Microsoft® Installer',
                             "Comment":'Wine installer utility for MSI packages',
                             "Type":TYPE,
                             "Exec":'wine msiexec /i %f',
                             "NoDisplay":'true',
                             "Icon":'wine-msiexec',
                             "Terminal":'false',
                             "StartupWMClass":'msiexec.exe',
                             "Categories":[WINE_CATEGORIES["wine"]]},
        VENDOR_ID+"-mime-msi":{"Name":'Microsoft® Windows Installer File',
                               "Type":TYPE,
                               "Exec":'wine %f',
                               "Hidden":'true',
                               "MimeType":["application/x-ole-storage", "text/mspg-legacyinfo"],
                               "Terminal":'false',
                               "Categories":[WINE_CATEGORIES["wine"]]}
    }

    # Desktop directory files
    WINE_DESKTOP_FILES = ["Wine", "Wine-Programs", "Wine-Programs-Accessories"]

    # Icon File Constants
    NEW_INKSCAPE_VERSION = "0.92"
    NEW_ICON_SIZE = 64
    ICONS_TARGET_RELPATH = "icons/"
    SVG_TARGET_RELPATH = os.path.join(ICONS_TARGET_RELPATH, "hicolor/scalable/")
    OVERLAY_LARGE_X_SCALE = '0.70'
    OVERLAY_LARGE_Y_SCALE = '0.66'
    OVERLAY_MEDIUM_X_SCALE = '0.48'
    OVERLAY_MEDIUM_Y_SCALE = '0.44'

    # Global Wine Logo Overlay icon
    WINE_LOGO_DIRECTORY = "dlls/user32/resources/"
    WINE_SVG_LOGO_FILENAME = "oic_winlogo.svg"
    WINE_ICON_LOGO_FILENAME = "oic_winlogo.ico"

    # Application icons
    SVG_APPS_TARGET_RELPATH = os.path.join(SVG_TARGET_RELPATH, 'apps/')
    APP_SVG_FILES = {'notepad.svg':{'srpath':'programs/notepad/',
                                    'trpath':SVG_APPS_TARGET_RELPATH},
                     'taskmgr.svg':{'srpath':'programs/taskmgr/',
                                    'trpath':SVG_APPS_TARGET_RELPATH},
                     'regedit.svg':{'srpath':'programs/regedit/',
                                    'trpath':SVG_APPS_TARGET_RELPATH},
                     'msiexec.svg':{'srpath':'programs/msiexec/',
                                    'trpath':SVG_APPS_TARGET_RELPATH},
                     WINE_SVG_LOGO_FILENAME:{
                         'srpath':WINE_LOGO_DIRECTORY,
                         'trpath':SVG_APPS_TARGET_RELPATH},
                     'winecfg.svg':{'srpath':'programs/winecfg/',
                                    'trpath':SVG_APPS_TARGET_RELPATH},
                     'winefile.svg':{'srpath':'programs/winefile/',
                                     'trpath':SVG_APPS_TARGET_RELPATH},
                     'winemine.svg':{'srpath':'programs/winemine/',
                                     'trpath':SVG_APPS_TARGET_RELPATH},
                     'wcmd.svg':{'srpath':'programs/cmd/',
                                 'trpath':SVG_APPS_TARGET_RELPATH},
                     'iexplore.svg':{'srpath':'programs/iexplore/',
                                     'trpath':SVG_APPS_TARGET_RELPATH},
                     'winhelp.svg':{'srpath':'programs/winhlp32/',
                                    'trpath':SVG_APPS_TARGET_RELPATH},
                     'wordpad.svg':{'srpath':'programs/wordpad/',
                                    'trpath':SVG_APPS_TARGET_RELPATH}
                    }

    # Place icons
    SVG_PLACES_TARGET_RELPATH = os.path.join(SVG_TARGET_RELPATH, 'places/')
    PLACES_SVG_FILES = {'document.svg':{'srpath':'dlls/shell32/',
                                        'trpath':SVG_PLACES_TARGET_RELPATH},
                        'mydocs.svg':{'srpath':'dlls/shell32/',
                                      'trpath':SVG_PLACES_TARGET_RELPATH},
                        'desktop.svg':{'srpath':'dlls/shell32/',
                                       'trpath':SVG_PLACES_TARGET_RELPATH},
                        'printer.svg':{'srpath':'dlls/shell32/',
                                       'trpath':SVG_PLACES_TARGET_RELPATH},
                        'drive.svg':{'srpath':'dlls/shell32/',
                                     'trpath':SVG_PLACES_TARGET_RELPATH},
                        'control.svg':{'srpath':'dlls/shell32/',
                                       'trpath':SVG_PLACES_TARGET_RELPATH},
                        'cdrom.svg':{'srpath':'dlls/shell32/',
                                     'trpath':SVG_PLACES_TARGET_RELPATH},
                        'netdrive.svg':{'srpath':'dlls/shell32/',
                                        'trpath':SVG_PLACES_TARGET_RELPATH},
                        'mycomputer.svg':{'srpath':'dlls/shell32/',
                                          'trpath':SVG_PLACES_TARGET_RELPATH}
                       }

    # Global icon id names
    LARGE_SVG_ICON_ID = 'icon:large-scaleable'
    MEDIUM_SVG_ICON_ID = 'icon:medium-scaleable'
    SMALL_SVG_ICON_ID = 'icon:small-scaleable'

    # Global SVG namespaces
    XMLNS = {'dc_uri':'http://purl.org/dc/elements/1.1/',
             'cc':'http://creativecommons.org/ns#',
             'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
             'xlink':'http://www.w3.org/1999/xlink',
             'sodipodi':'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
             'inkscape':'http://www.inkscape.org/namespaces/inkscape',
             'svg':'http://www.w3.org/2000/svg'}

    # Main Directories
    SUBDIRECTORIES = ["applications", "desktop-directories", "icons", "xdg"]
