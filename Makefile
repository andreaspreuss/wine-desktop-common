MENU_FILES  =  \
	xdg/wine.menu \
	xdg/x-wine.menu

DESKTOP_FILES  =  \
	applications/wine-mime-msi.desktop \
	applications/wineboot.desktop \
	applications/winebrowsecdrive.desktop \
	applications/winecfg.desktop \
	applications/winecmd.desktop \
	applications/winecontrol.desktop \
	applications/wineexplorer.desktop \
	applications/winefile.desktop \
	applications/wineiexplore.desktop \
	applications/winemine.desktop \
	applications/winemsiexec.desktop \
	applications/winenotepad.desktop \
	applications/wineoleview.desktop \
	applications/wineregedit.desktop \
	applications/winetaskmgr.desktop \
	applications/wineuninstaller.desktop \
	applications/winewinhelp.desktop \
	applications/winewordpad.desktop

DIRECTORY_FILES  =  \
	desktop-directories/wine-programs-accessories.directory \
	desktop-directories/wine-programs.directory \
	desktop-directories/wine.directory

APPS_ICONS  =  \
	icons/hicolor/scalable/apps/wine-iexplore.svg \
	icons/hicolor/scalable/apps/wine-msiexec.svg \
	icons/hicolor/scalable/apps/wine-notepad.svg \
	icons/hicolor/scalable/apps/wine-regedit.svg \
	icons/hicolor/scalable/apps/wine-taskmgr.svg \
	icons/hicolor/scalable/apps/wine-wcmd.svg \
	icons/hicolor/scalable/apps/wine-winecfg.svg \
	icons/hicolor/scalable/apps/wine-winefile.svg \
	icons/hicolor/scalable/apps/wine-winemine.svg \
	icons/hicolor/scalable/apps/wine-winhelp.svg \
	icons/hicolor/scalable/apps/wine-wordpad.svg \
	icons/hicolor/scalable/apps/wine.svg

PLACES_ICONS  =  \
	icons/hicolor/scalable/places/cdrom-wine.svg \
	icons/hicolor/scalable/places/control-wine.svg \
	icons/hicolor/scalable/places/desktop-wine.svg \
	icons/hicolor/scalable/places/document-wine.svg \
	icons/hicolor/scalable/places/drive-wine.svg \
	icons/hicolor/scalable/places/mycomputer-wine.svg \
	icons/hicolor/scalable/places/mydocs-wine.svg \
	icons/hicolor/scalable/places/netdrive-wine.svg \
	icons/hicolor/scalable/places/printer-wine.svg

WINE_ICO = icons/oic_winlogo.ico

all: $(MENU_FILES) $(DESKTOP_FILES) $(DIRECTORY_FILES) $(APPS_ICONS) $(PLACES_ICONS) $(WINE_ICO)

install: all
	install -d "$(DESTDIR)$(EPREFIX)/etc/xdg/menus/applications-merged"
	install -m0644 $(MENU_FILES) "$(DESTDIR)$(EPREFIX)/etc/xdg/menus/applications-merged"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/applications"
	install -m0644 $(DESKTOP_FILES) "$(DESTDIR)$(EPREFIX)/usr/share/applications"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/desktop-directories"
	install -m0644 $(DIRECTORY_FILES) "$(DESTDIR)$(EPREFIX)/usr/share/desktop-directories"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/apps"
	install -m0644 $(APPS_ICONS) "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/apps"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/places"
	install -m0644 $(PLACES_ICONS) "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/places"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/wine/icons"
	install -m0644 $(WINE_ICO) "$(DESTDIR)$(EPREFIX)/usr/share/wine/icons"
