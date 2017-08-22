MENU_FILES = /home/robert_gentoo/Packages/Gentoo/wine-desktop-common/xdg/wine.menu

DESKTOP_FILES = \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-iexplore.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-explorer.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-cmd.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-winecfg.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-browsedrive.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-notepad.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-wordpad.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-regedit.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-uninstaller.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-msiexec.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-winhelp.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-wineboot.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-mime-msi.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-winemine.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-control.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-winefile.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-taskmgr.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-browsecdrive.desktop \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/applications/wine-oleview.desktop

DIRECTORY_FILES = \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/desktop-directories/wine-wine.directory \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/desktop-directories/wine-Programs.directory \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/desktop-directories/wine-Programs-Accessories.directory

ICONS = \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/control-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/desktop-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/cdrom-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/netdrive-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/printer-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/mycomputer-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/mydocs-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/drive-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/places/document-wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-notepad.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-winhelp.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-wordpad.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-winemine.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-iexplore.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-winecfg.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-winefile.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-regedit.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-wcmd.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-msiexec.svg \
	/home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/hicolor/scalable/apps/wine-taskmgr.svg

WINE_ICO = /home/robert_gentoo/Packages/Gentoo/wine-desktop-common/icons/oic_winlogo.ico

all: $(MENU_FILES) $(DESKTOP_FILES) $(DIRECTORY_FILES) $(ICONS) $(WINE_ICO)

install: all
	install -d "$(DESTDIR)$(EPREFIX)/etc/xdg/menus/applications-merged"
	install -m0644 $(MENU_FILES) "$(DESTDIR)$(EPREFIX)/etc/xdg/menus/applications-merged"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/applications"
	install -m0644 $(DESKTOP_FILES) "$(DESTDIR)$(EPREFIX)/usr/share/applications"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/desktop-directories"
	install -m0644 $(DIRECTORY_FILES) "$(DESTDIR)$(EPREFIX)/usr/share/desktop-directories"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/apps"
	install -m0644 icons/hicolor/scalable/apps/* "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/apps"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/places"
	install -m0644 icons/hicolor/scalable/places/* "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/scalable/places"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/wine/icons"
	install -m0644 $(WINE_ICO) "$(DESTDIR)$(EPREFIX)/usr/share/wine/icons"
