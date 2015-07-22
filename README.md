# python-tesseract
This project has been automatically exported from [here](https://code.google.com/p/python-tesseract)
This setup document has been taken from [here](https://code.google.com/p/python-tesseract/wiki/HowToCompile)

How to compile python-tesseract for Ubuntu, Mac OSX and Cygwin
==============================================================

This library is the first step of a journey that every markup file in a repository goes on before it is rendered on GitHub.com:

0. This library converts the raw markup to HTML. See the list of [supported markup formats](#markups) below.
0. The HTML is sanitized, aggressively removing things that could harm you and your kin—such as `script` tags, inline-styles, and `class` or `id` attributes. See the [sanitization filter](https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/sanitization_filter.rb) for the full whitelist.
0. Syntax highlighting is performed on code blocks. See [github/linguist](https://github.com/github/linguist#syntax-highlighting) for more information about syntax highlighting.
0. The HTML is passed through other filters in the [html-pipeline](https://github.com/jch/html-pipeline) that add special sauce, such as [emoji](https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/emoji_filter.rb), [task lists](https://github.com/github/task_list/blob/master/lib/task_list/filter.rb), [named anchors](https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb), [CDN caching for images](https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/camo_filter.rb), and  [autolinking](https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/autolink_filter.rb).
0. The resulting HTML is rendered on GitHub.com.

Please see our [contributing guidelines](CONTRIBUTING.md) before reporting an issue.

How to compile python-tesseract (for Ubuntu Raring & Saucy & Trusty )
---------------------------------------------------------------------
```
sudo apt-get install python-distutils-extra tesseract-ocr tesseract-ocr-eng libopencv-dev libtesseract-dev libleptonica-dev python-all-dev swig libcv-dev python-opencv python-numpy python-setuptools python3-all-dev  build-essential subversion python3-setuptools
svn checkout http://python-tesseract.googlecode.com/svn/trunk/src python-tesseract
cd python-tesseract
python config.py
python setup.py clean
python setup.py build
python setup.py install --user
cd test-slim
export PYTHONPATH=$PYTHONPATH:$HOME/.local/lib/python2.7/site-packages
python test.py
```

==to make deb==
```
sudo apt-get install cdbs dh-buildinfo devscripts python-stdeb
dch -i
debuild binary
debuild -i -us -uc -b
debuild -ai386 -us -uc -b
```
==cross-compile i386==
```
sudo apt-get install pbuilder
sudo pbuilder --create --architecture i386
sudo pbuilder --login --save-after-login
sudo pbuilder --build python-tesseract_0.9-0.5ubuntu2.dsc
```
How to compile python-tesseract (for Ubuntu Oneiric)
----------------------------------------------------
```
sudo apt-get install tesseract-ocr-eng tesseract-ocr-dev libleptonica-dev python-all-dev swig libcv-dev
tar zxvf python-tesseract-xxxx.tar.gz
cd python-tesseract
python config.py
python setup.py clean
python setup.py build
sudo python setup.py install
```
==to make deb==
```
sudo apt-get install cdbs dh-buildinfo
./buildDeb
```

How to compile python-tesseract (for Ubuntu Natty)
--------------------------------------------------
```
sudo add-apt-repository ppa:nutznboltz/tesseract
sudo apt-get update
sudo apt-get install tesseract-ocr-dev leptonica python-all-dev swig
tar zxvf python-tesseract-xxxx.tar.gz
cd python-tesseract
python config.py
python setup.py clean
python setup.py build
sudo python setup.py install
```
==to make deb==
```
sudo python setup.py --command-packages=stdeb.command sdist_dsc debianize bdist_deb 
```
How to compile python-tesseract (for Mac OS X Lion)
---------------------------------------------------

First, install tesseract svn as suggested by mcradle
(http://mousecradle.wordpress.com/2011/05/17/compiling-svn-tesseract-on-osx/)
Then,
```
sudo port select python python27
sudo port uninstall opencv
sudo port install py27-numpy
sudo port install opencv +python27
sudo port install leptonica swig swig-python 
export LDFLAGS="-L/opt/local/lib"
tar zxvf python-tesseract-xxxx.tar.gz
cd python-tesseract
python config.py
python setup.py clean
python setup.py build
sudo python setup.py install
```
If you ran into "Segmentation fault 11" then following the steps suggested by Solem
(http://www.janeriksolem.net/2011/12/installing-opencv-python-interface-on.html)

How to compile python-tesseract from svn version of tesseract-ocr
-------------------------------------------------------------------
For cygwin Only
1. Install cygwin by starting setup.exe
2. then install subversion and wget
3. start cygwin-bash-shell
```
svn --force export http://apt-cyg.googlecode.com/svn/trunk/src /bin/
chmod +x /bin/apt-cyg
apt-cyg install nano make autobuild libtool libiconv gcc4 libtiff-devel libpng14-devel libgif-devel libSM-devel libjbig-devel
```
For Natty
```
apt-get build-dep tesseract-ocr leptonica
```
For both Natty and Cygwin
1. compile and link webp and leptonica
```
wget http://webp.googlecode.com/files/libwebp-0.1.3.tar.gz
tar zxvf libwebp-0.1.3.tar.gz
cd libwebp-0.1.3
./autogen.sh
./configure LDFLAGS="-no-undefined  -Wl,--as-needed" --prefix=/usr
make clean && make -j 4 && make install
cd ..

wget http://leptonica.googlecode.com/files/leptonica-1.68.tar.gz
tar zxvf leptonica-1.68.tar.gz
cd leptonica-1.68
./autobuild
./configure LDFLAGS="-no-undefined  -Wl,--as-needed" --prefix=/usr
make clean && make -j 4 && make install
cd ..
```
2. compile and link tesseract-ocr
```
sudo apt-get install libtiff-dev libjpeg-dev libpng-dev subversion devscripts build-essential debhelper autoconf automake libtool libleptonica-dev
```

Static Build(easy)
```
svn checkout http://tesseract-ocr.googlecode.com/svn/trunk/src tesseract-ocr-read-only
cd tesseract-ocr-read-only
./autogen.sh --prefix=/usr
./configure --prefix=/usr --disable-shared
make clean && make -j 4 && make install
cd ..
```
Shared Build(difficult)
Cygwin is buggy on producing shared library.
```
svn checkout http://tesseract-ocr.googlecode.com/svn/trunk/src tesseract-ocr-read-only
cd tesseract-ocr-read-only
#wget http://python-tesseract.googlecode.com/files/fix_ugly_cygwin_bug.diff
#patch -p0 -i fix_ugly_cygwin_bug.diff
./autogen.sh --prefix=/usr
./configure LDFLAGS="-no-undefined  -Wl,--as-needed" --prefix=/usr
make clean && make "USING_MULTIPLELIBS=1" && make install 
```
3. Make python-tesseract
```
svn checkout http://python-tesseract.googlecode.com/svn/trunk/src python-tesseract
cd python-tesseract
#apt-cyg install swig python #for cygwin only
#apt-get install swig python # for natty only
python setup.py build
python setup.py install
```


