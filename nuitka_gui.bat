cd c:\temp

python -m nuitka ^
    --onefile ^
    --plugin-enable=pkg-resources ^
    --plugin-enable=pyside6 ^
    --windows-disable-console ^
    --windows-icon-from-ico=weather.ico ^
    owm_gui.py
pause