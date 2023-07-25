python datasets/uuider.py

echo f | xcopy /y "%~dp0datasets\charger_rate_historic.csv" "%~dp0database\charger_rate_historic.csv"
echo f | xcopy /y "%~dp0datasets\chargers_connectors_modded.csv" "%~dp0database\chargers_connectors_modded.csv"
echo f | xcopy /y "%~dp0datasets\chargers_modded.csv" "%~dp0database\chargers_modded.csv"
echo f | xcopy /y "%~dp0datasets\connectors_modded.csv" "%~dp0database\connectors_modded.csv"

del "%~dp0\datasets\charger_rate_historic.csv"
del "%~dp0\datasets\chargers_connectors_modded.csv"
del "%~dp0\datasets\chargers_modded.csv"
del "%~dp0\datasets\connectors_modded.csv"

pause