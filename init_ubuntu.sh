#!/bin/sh

TZ="Europe/Warsaw"
DEBIAN_FRONTEND=noninteractive

apt update > /dev/null
apt install --yes markdown > /dev/null
cd /source

echo '<!DOCTYPE html>' > index.html
echo '<html lang="en-US">' >> index.html
cat docs/head.html >> index.html

echo '<body>' >> index.html
markdown README.md >> index.html
echo '</body>' >> index.html
echo '</html>' >> index.html

apt install --yes python3-pip linux-headers-5.19.0-38-generic build-essential python3-dev xvfb appstream tar lsb-release apt-utils file upx > /dev/null

pip install --upgrade wheel setuptools > /dev/null
pip install -r requirements.txt > /dev/null
pip install pyinstaller > /dev/null

Xvfb -ac :0 -screen 0 1280x1024x24 &
sleep 5

py_deps_editor=""
for X in $(cat requirements.txt); do
    py_deps_editor=$py_deps_editor' --collect-all '$X
done

py_deps_editor=$py_deps_editor' --collect-all tkinter'

for X in $(find . -name '__pycache__'); do
    rm -rf "$X"
done

py_data_editor=""
for X in ./editor/*; do
    if [ -f "$X" ]; then
        BASENAME=$(basename "$X")
        py_data_editor=$py_data_editor" --add-data $BASENAME:."
    fi
done

py_dirs_editor=""
for X in ./editor/*; do
    if [ -d "$X" ]; then
        BASENAME=$(basename "$X")
        py_dirs_editor=$py_dirs_editor" --add-data $BASENAME/*:$BASENAME/"
    fi
done

python3 setup.py build
python3 setup.py install

cd editor

DISPLAY=":0" pyinstaller -F --onefile --console \
 --additional-hooks-dir=. $py_dirs_editor $py_data_editor \
  $py_deps_editor -i ../docs/icon.png -n editor -c standalone.py

mv dist/editor ../editor-glibc
rm -rf dist build log

cd ..

strip editor-glibc

chmod +x editor-glibc

mkdir -p editor.AppDir/var/lib/dpkg
mkdir -p editor.AppDir/var/cache/apt/archives
apt install --yes debootstrap fakeroot fakechroot
fakechroot fakeroot debootstrap --variant=fakechroot --arch amd64 22.04 /source/editor.AppDir/ http://archive.ubuntu.com/ubuntu > /dev/null

cd editor.AppDir/
rm -rf etc var home mnt srv proc sys boot opt
cd ..

cp docs/icon.png editor.AppDir/icon.png

echo '[Desktop Entry]' > editor.AppDir/editor.desktop
echo 'Name=editor' >> editor.AppDir/editor.desktop
echo 'Categories=Settings' >> editor.AppDir/editor.desktop
echo 'Type=Application' >> editor.AppDir/editor.desktop
echo 'Icon=icon' >> editor.AppDir/editor.desktop
echo 'Terminal=true' >> editor.AppDir/editor.desktop
echo 'Exec=/usr/bin/editor' >> editor.AppDir/editor.desktop

chmod +x editor.AppDir/editor.desktop

echo '#!/bin/sh' > editor.AppDir/AppRun
echo 'editor_RUNPATH="$(dirname "$(readlink -f "${0}")")"' >> editor.AppDir/AppRun
echo 'editor_EXEC="${editor_RUNPATH}"/usr/bin/editor' >> editor.AppDir/AppRun
echo 'export LD_LIBRARY_PATH="${editor_RUNPATH}"/lib:"${editor_RUNPATH}"/lib64:$LD_LIBRARY_PATH' >> editor.AppDir/AppRun
echo 'export LIBRARY_PATH="${editor_RUNPATH}"/lib:"${editor_RUNPATH}"/lib64:"${editor_RUNPATH}"/usr/lib:"${editor_RUNPATH}"/usr/lib64:$LIBRARY_PATH' >> editor.AppDir/AppRun
echo 'export PATH="${editor_RUNPATH}/usr/bin/:${editor_RUNPATH}/usr/sbin/:${editor_RUNPATH}/usr/games/:${editor_RUNPATH}/bin/:${editor_RUNPATH}/sbin/${PATH:+:$PATH}"' >> editor.AppDir/AppRun
echo 'exec "${editor_EXEC}" "$@"' >> editor.AppDir/AppRun

chmod +x editor.AppDir/AppRun

mkdir -p editor.AppDir/usr/bin
cp editor-glibc editor.AppDir/usr/bin/editor
chmod +x editor.AppDir/usr/bin/editor

wget -q https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage -O toolkit.AppImage
chmod +x toolkit.AppImage

cd /opt/
/source/toolkit.AppImage --appimage-extract
mv /opt/squashfs-root /opt/appimagetool.AppDir
ln -s /opt/appimagetool.AppDir/AppRun /usr/local/bin/appimagetool
chmod +x /opt/appimagetool.AppDir/AppRun
cd /source

ARCH=x86_64 appimagetool editor.AppDir/

mv editor-x86_64.AppImage editor-glibc-x86_64.AppImage

rm -rf editor.AppDir
rm -f toolkit.AppImage
rm -rf editor.egg-info
chmod +x editor-glibc-x86_64.AppImage

sha256sum editor-glibc > sha256sum.txt
sha256sum editor-glibc-x86_64.AppImage >> sha256sum.txt

mkdir -pv /runner/page/
cp -rv /source/* /runner/page/