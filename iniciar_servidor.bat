@echo off
title Servidor Resgautte - MisticPay Gateway
cls
echo ============================================================
echo       INICIANDO SERVIDOR WEB RESGAUTTE COM MISTICPAY
echo ============================================================
echo.
echo Abrindo navegador em http://localhost:3000 ...
start http://localhost:3000
echo.
python server.py
pause
