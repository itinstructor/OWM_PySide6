cd c:\temp

python -m nuitka ^
    --onefile ^
    --enable-plugin=anti-bloat ^
    --enable-plugin=pyside6 ^
    --windows-disable-console ^
    --windows-icon-from-ico=weather.ico ^
    owm_qt.py
pause