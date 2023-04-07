..\robot.exe -f -m ..\maps\1.txt "python TeamCode\main.py" > r.log
timeout /t 1
..\robot.exe -f -m ..\maps\2.txt "python TeamCode\main.py" >> r.log
timeout /t 1
..\robot.exe -f -m ..\maps\3.txt "python TeamCode\main.py" >> r.log
timeout /t 1
..\robot.exe -f -m ..\maps\4.txt "python TeamCode\main.py" >> r.log
