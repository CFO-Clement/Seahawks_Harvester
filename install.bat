@echo off
setlocal enabledelayedexpansion

set ENV_FILE=./config.env

:configure_env
set /p HARVESTER_NAME=Entrez le nom (identifiant) de l'Harvester (HARVESTER_NAME):
set /p HARVESTER_FREQUENCY=Entrez la frequence de l'Harvester (HARVESTER_FREQUENCY):
set /p NESTER_ENDPOINT=Entrez l'host (ip) du Nester (NESTER_ENDPOINT):
set /p NESTER_PORT=Entrez le port du Nester (NESTER_PORT):

echo HARVESTER_NAME=!HARVESTER_NAME! > %ENV_FILE%
echo HARVESTER_FREQUENCY=!HARVESTER_FREQUENCY! >> %ENV_FILE%
echo NESTER_ENDPOINT=!NESTER_ENDPOINT! >> %ENV_FILE%
echo NESTER_PORT=!NESTER_PORT! >> %ENV_FILE%
goto main

:build_compose
docker-compose --env-file %ENV_FILE% build
goto :eof

:build_dockerfile
docker build -t harverster_image .
goto :eof

:main
if "%~1" neq "" (
    if "%1" == "compose" (
        call :build_compose
    ) else if "%1" == "docker" (
        call :build_dockerfile
    ) else (
        echo Argument invalide: %1
        echo Utilisation: %0 [compose|docker]
        exit /b 1
    )
) else (
    echo Bienvenue dans le script d'installation
    echo 1. Configurer les variables d'environnement
    echo 2. Construire avec Docker Compose
    echo 3. Construire avec Dockerfile
    set /p choice=Choisissez une option:

    if "!choice!"=="1" (
        call :configure_env
    ) else if "!choice!"=="2" (
        call :build_compose
    ) else if "!choice!"=="3" (
        call :build_dockerfile
    ) else (
        echo Option invalide.
        exit /b 1
    )
)

echo Installation terminee.
