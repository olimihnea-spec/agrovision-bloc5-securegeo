@echo off
cd /d "G:\CLAUDE CODE INSTRUIRE VOL II 90 ZILE STREAMLIT ISI YOLO\Bloc5_AI_Aplicat\ai_app"
echo Pornesc SecureGeo Platform...
echo Dupa pornire, deschide browser la: http://localhost:8501
echo Pagina SecureGeo: sectiunea din stanga - "10b SecureGeo Platform"
echo.
python -m streamlit run Acasa.py --server.port 8501
pause
