@echo off
echo ========================================
echo    超级马里奥游戏 - 程序打包
echo ========================================
echo.
echo 正在打包程序,请稍候...
echo.

REM 使用PyInstaller打包程序
pyinstaller --name="超级马里奥游戏" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data "README.md;." ^
    mario_game.py

echo.
echo ========================================
echo 打包完成!
echo ========================================
echo.
echo 可执行文件位置: dist\超级马里奥游戏.exe
echo.
echo 你可以直接运行 dist 文件夹中的 exe 文件
echo.
pause
