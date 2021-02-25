@echo off
:: Run python 2 script...

call conda activate %3

python -c "import sys; sys.path.append(r""%1""); from py2_whisk import CreateWhiskPickles ; CreateWhiskPickles(r""%2"")"
goto :eof