# wine-desktop-common

[![Build Status](https://travis-ci.org/bobwya/wine-desktop-common.svg?branch=master)](https://travis-ci.org/bobwya/wine-desktop-common) [![License](http://img.shields.io/:license-lgpl-green.svg)](https://tldrlegal.com/license/gnu-lesser-general-public-license-v2.1-(lgpl-2.1))

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

## Troubleshooting

If your Desktop Environment menus or panel still show low-resolution icons for Wine desktop entries...
Then you may want to purge any old, low resolution **png** icons from your local user Freedesktop XDG directories, e.g.:

```
find "${HOME}/.local/share/icons/hicolor" -type f -iregex ".*\(iexplore\|notepad\|wordpad\)\.0\.png" -print0 | xargs -0 rm -f
```

## Build Information

Uses a custom Python 3.6 script to:

 * extract and cleanup a set of scalable Wine icons, from a local copy of the Wine Source tree
 * automatically generate a complete suite of wine .desktop and .menu files, with broad locale support

LGPL-2.1 license for Wine icons.
