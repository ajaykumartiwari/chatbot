@echo off
color 0D
REM title Connect Chatbot with a Database
REM echo Select one of the Database
REM set /p option="1. MongoDB  2. MySql  3. Cassandra  4.Neo4j : "
REM if "%option%"=="1" echo MongoDB Connected
REM if "%option%"=="2" echo Please Install MySql Database

:choice
set /P c=Do you want to continue [Y/N]?
if /I "%c%" EQU "Y" goto :yes
if /I "%c%" EQU "N" goto :no
goto :choice

:yes
echo Select one of the Database
set /p option="1. MongoDB  2. MySql  3. Cassandra  4.Neo4j : "
if "%option%"=="1" python "D:\Python\FLASK-NLP-POC\ChatBot_POC\chatbot_nlp_mongo\chatbot-v2\app\DbConfig\mongodb.py"
if "%option%"=="2" echo Please Install MySql Database 
goto :continue

:no
echo "User has typed no"

:continue
pause