@echo off
:: Run python 2 script...
if "%1"=="" goto error


cd %1

trace %2.avi %2.whiskers
measure --face %3 %2.whiskers %2.measurements
classify %2.measurements %2.measurements %3 --px2mm %4 -n %5

goto :eof

:error
@echo couldn't run whisk because of a lack of arguments