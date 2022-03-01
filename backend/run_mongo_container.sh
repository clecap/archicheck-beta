#!/bin/bash

helpDoc='
USAGE:
       ./run_mongo_container.sh [-t] | [-p] | [-r] | [-x FILE] | [-i FILE]
        | [-h]

OPTIONS
       -t, --temporary
              No persistence. Remove the database volume after the container
              has stopped. The persistent volume used in the `-p` option is
              not affected by that.

       -p, --persistent
              Keep the volume after container shutdown. The default volume
              name is `archicheck-volume`. The next call in `--persistent`
              mode will have the same DB content. Other containers started
              in `--temporary` mode will not affect this persistent volume.

       -r, --reset
              Stop running container (if any) and reset (and remove) the
              `archicheck-volume`.
              
       -x, --export-volume [FILE]
              Only works if the container has been started in persistent mode.
              Shut down the currently running container (if any) and export
              the current DB to FILE, so it can be import again on another
              host machine. If no FILE is provided, it will export to
              `db_dump.tar` by default. It is recommended to use ".tar" as
              file name suffix because that will be ignored by git and the
              docker build daemon, which speeds up the web server container
              start.

       -i, --import-volume FILE
              Import the given FILE into the `archicheck-volume` and start the
              container.

       -h, --help
              Print this help.
'
set -e


# Read DB credentials into shell variables:
. db.conf

if [[ -z "$1" ]]; then
    echo "No parameter provided."
    echo "$helpDoc"
    exit
fi
if [[ "$1" == "-t" || "$1" == "--temporary" ]]; then
    echo "Starting container with temporary volume, will be deleted after container has stopped..."
    docker run --name archicheck-DB --network archicheck-network -e MONGO_INITDB_ROOT_USERNAME="$dbusername" -e MONGO_INITDB_ROOT_PASSWORD="$dbpassword" -d --rm mongo:5.0
    exit

elif [[ "$1" == "-p" || "$1" == "--persistent" ]]; then
    echo "Running in persistent mode: Mounting archicheck-volume into container..."
    # Start DB container with mounted volume:
    docker run --name archicheck-DB --network archicheck-network -v archicheck-volume:/data/db -e MONGO_INITDB_ROOT_USERNAME="$dbusername" -e MONGO_INITDB_ROOT_PASSWORD="$dbpassword" -d --rm mongo:5.0
    exit

elif [[ "$1" == "-r" || "$1" == "--reset" ]]; then
    echo "Stopping running container..."
    docker stop archicheck-DB > /dev/null && echo "Container stopped." || echo "Container was not running. Fine."
    echo "Resetting/deleting the persistent volume..."
    docker volume rm archicheck-volume > /dev/null && echo "Persistent volume has been deleted." || echo "Could not remove volume."
    exit

elif [[ "$1" == "-x" || "$1" == "--export-volume" ]]; then
    # Check if container is running:
    echo "Stopping running db container..."
    docker stop archicheck-DB > /dev/null && echo "Stopped container." || echo "DB container was not running. Fine. Continuing with volume export..."


    # Check if volume exists:
    volume_missing=0
    docker volume inspect archicheck-volume >/dev/null || volume_missing=1
    if [[ volume_missing -eq 0 ]]; then
        
        exportFile="db_dump.tar"
        if [[ -n $2 ]]; then
            exportFile="$2"
        fi

        echo "Exporting DB volume to '$exportFile'..."
        # Convert to relative path:
        exportFile=$(realpath --relative-to=. "$exportFile")
        docker run --rm -v archicheck-volume:/dbdata -v "$(pwd)":/backup busybox tar cvf /backup/"$exportFile" /dbdata > /dev/null
        echo "Success."
    else
        echo "Volume does not exist, so it cannot be exported. Exiting."
    fi
    exit

elif [[ "$1" == "-i" || "$1" == "--import-volume" ]]; then
    echo -n "Importing volume. This will override the existing 'archicheck-volume' (if any). Continue? [y/n]"
    read -r decision
    if [[ $decision != "y" ]]; then
        echo "Exiting.."
        exit

    else
        if [[ -n $2 ]]; then
            importFile="$2"
            # Create a fresh container (and the associated volume):
            ./run_mongo_container.sh -r
            ./run_mongo_container.sh -p
            echo "Stopping container so DB can be imported..."
            docker stop archicheck-DB > /dev/null
            
            echo "Importing $importFile."
            # Convert to relative path:
            importFile=$(realpath --relative-to=. "$importFile")
            docker run --rm -v archicheck-volume:/data/db -v "$(pwd)":/backup busybox sh -c "cd /data/db && tar xvf /backup/$importFile --strip 1" > /dev/null
            
            ./run_mongo_container.sh -p
            echo "Import success. Container is running."
        else
            echo "No import file provided. Exiting."
            exit
        fi
    fi



elif [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "$helpDoc"
    exit

fi
