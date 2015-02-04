MENU_FILES = xdg/wine.menu

DESKTOP_FILES = \
	applications/wine-browsedrive.desktop \
	applications/wine-notepad.desktop \
	applications/wine-uninstaller.desktop \
	applications/wine-winecfg.desktop

DIRECTORY_FILES = \
	desktop-directories/wine-Programs-Accessories.directory \
	desktop-directories/wine-Programs.directory \
	desktop-directories/wine-wine.directory

PNG_SIZES = 16x16 22x22 24x24 32x32 48x48

ICONS = \
	$(foreach size,$(PNG_SIZES),icons/hicolor/$(size)/apps/wine.png) \
	$(foreach size,$(PNG_SIZES),icons/hicolor/$(size)/apps/wine-notepad.png) \
	$(foreach size,$(PNG_SIZES),icons/hicolor/$(size)/apps/wine-uninstaller.png) \
	$(foreach size,$(PNG_SIZES),icons/hicolor/$(size)/apps/wine-winecfg.png) \
	$(foreach size,$(PNG_SIZES),icons/hicolor/$(size)/places/folder-wine.png) \
	icons/hicolor/scalable/apps/wine.svg \
	icons/hicolor/scalable/apps/wine-notepad.svg \
	icons/hicolor/scalable/apps/wine-uninstaller.svg \
	icons/hicolor/scalable/apps/wine-winecfg.svg

all: $(MENU_FILES) $(DESKTOP_FILES) $(DIRECTORY_FILES) $(ICONS)
install: all
	install -d "$(DESTDIR)$(EPREFIX)/etc/xdg/menus/applications-merged"
	install -m0644 $(MENU_FILES) "$(DESTDIR)$(EPREFIX)/etc/xdg/menus/applications-merged"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/applications"
	install -m0644 $(DESKTOP_FILES) "$(DESTDIR)$(EPREFIX)/usr/share/applications"
	install -d "$(DESTDIR)$(EPREFIX)/usr/share/desktop-directories"
	install -m0644 $(DIRECTORY_FILES) "$(DESTDIR)$(EPREFIX)/usr/share/desktop-directories"
	for size in 16x16 22x22 24x24 32x32 48x48 scalable; do \
		install -d "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/$$size/apps"; \
		install -m0644 icons/hicolor/$$size/apps/* "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/$$size/apps"; \
	done
	for size in 16x16 22x22 24x24 32x32 48x48; do \
		install -d "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/$$size/places"; \
		install -m0644 icons/hicolor/$$size/places/* "$(DESTDIR)$(EPREFIX)/usr/share/icons/hicolor/$$size/places"; \
	done
