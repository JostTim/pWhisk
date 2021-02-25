@echo off
:: Run python 2 script...

call conda activate %3

python -c "import sys; sys.path.append(r""%1""); from WhiskReadings import Measurements_to_Pickle ; Measurements_to_Pickle(r""%2"")"
goto :eof