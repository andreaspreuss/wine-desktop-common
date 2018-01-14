# wine-desktop-common

Distribution agnostic Wine desktop and icon files common to all Wine packages in the **Gentoo** **GNU/Linux** **::bobwya** Overlay.

## Installation on non-Gentoo Linux Distributions

To install these desktop integration files on any standard Linux distribution (e.g. **Debian**/**Ubuntu**, **Fedora**, **OpenSUSE**, **Arch Linux**), other than **Gentoo**:

```
cd ~/Downloads
wget -O wine-desktop-common-master.tar.gz https://github.com/bobwya/wine-desktop-common/archive/master.tar.gz
tar xvfa wine-desktop-common-master.tar.gz
cd wine-desktop-common-master
sudo make install
```

## Build Information

Uses custom BASH scripts to:

 * extract a set of scalable Wine icons, from the Wine Git tree
 * automatically generate a complete suite of wine .desktop files, with broad locale support

LGPL-2.1 license for Wine icons.
