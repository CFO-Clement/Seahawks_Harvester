#!/bin/bash

ENV_FILE="./config.env"

configure_env() {
    read -p "Entrez le nom (identifiant) de l'Harvester (HARVESTER_NAME): " HARVESTER_NAME
    read -p "Entrez la frequence de l'Harvester (HARVESTER_FREQUENCY): " HARVESTER_FREQUENCY
    read -p "Entrez l'host (ip) du Nester (NESTER_ENDPOINT): " NESTER_ENDPOINT
    read -p "Entrez le port du Nester (NESTER_PORT): " NESTER_PORT

    echo "HARVESTER_NAME=${HARVESTER_NAME}" > ${ENV_FILE}
    echo "HARVESTER_FREQUENCY=${HARVESTER_FREQUENCY}" >> ${ENV_FILE}
    echo "NESTER_ENDPOINT=${NESTER_ENDPOINT}" >> ${ENV_FILE}
    echo "NESTER_PORT=${NESTER_PORT}" >> ${ENV_FILE}
    main
}

build_compose() {
    sudo docker-compose --env-file ${ENV_FILE} build
}

build_dockerfile() {
    sudo docker build -t harverster_image .
}

main() {
    if [ "$#" -gt 0 ]; then
        if [ "$1" = "compose" ]; then
            build_compose
        elif [ "$1" = "docker" ]; then
            build_dockerfile
        else
            echo "Argument invalide: $1"
            echo "Utilisation: $0 [compose|docker]"
            exit 1
        fi
    else
        echo "Bienvenue dans le script d'installation"
        echo "1. Configurer les variables d'environnement"
        echo "2. Construire avec Docker Compose"
        echo "3. Construire avec Dockerfile"
        read -p "Choisissez une option: " choice

        case $choice in
            1)
                configure_env
                ;;
            2)
                build_compose
                ;;
            3)
                build_dockerfile
                ;;
            *)
                echo "Option invalide."
                exit 1
                ;;
        esac
    fi

    echo "Installation terminée."
}
main
