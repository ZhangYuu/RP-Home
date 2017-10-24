#!/bin/bash

COLOR='\033[1;36m'          # bold;cyan
COLOR_WARNING='\033[1;33m'  # bold;yellow
COLOR_PROMPT='\033[1;32m'   # bold;green
COLOR_ERROR='\033[1;31m'    # bold;red
NO_COLOR='\033[0m'

# regex to capture any integer number
IS_NUMBER='^[0-9]+$'

KILL_FLAG=0
TIME_OUT=0

while [ "${1}" != "" ]; do
    case ${1} in
        -h | --help )
            echo "USAGE: ./run.sh [-k | --kill]"
            exit 0
            ;;
        -k | --kill )
            KILL_FLAG=1
            shift
            ;;
        # -l | --log )
        #     KEEP_LOG=1
        #     shift
        #     ;;
        # -s | --status )
        #     STATUS_FLAG=1
        #     shift
        #     ;;
        -t | --timeout )
            shift
            if [[ ${1} =~ ${IS_NUMBER} ]]
            then
                TIME_OUT=${1}
                echo -e "${COLOR_WARNING}TIMEOUT : ${TIME_OUT} sec${NO_COLOR}"
            fi
            shift
            ;;
        *) # default:
            echo
            echo -e "RUN: ${COLOR_ERROR}error:${NO_COLOR} ${1} option is not available (please see usage with -h or --help)"
            echo
            exit 1
            ;;
    esac
done

if [ ${KILL_FLAG} -eq 0 ];
then
    echo -e ${COLOR}
    echo -ne "RP-Home is starting up..."
    echo -e ${NO_COLOR}

    export FLASK_APP=__init__.py

    echo | nohup ./ngrok http 5000 &

    echo | nohup flask run --host=0.0.0.0 --port=5000 &
    
    for (( i=3 ; i>=1 ; i-- ))
    do
        echo -ne "Starting application... ${i}\033[0K\r"
        sleep 1
    done

    curl http://localhost:4040/api/tunnels \
    | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"
    # | mail -s 'Your Link to RP-Home' wxu16@stevens.edu

    if [ ${TIME_OUT} -gt 0 ];
    then
        echo -n "Timeout is counting down (${TIME_OUT} sec)..."
        sleep ${TIME_OUT}s
        KILL_FLAG=1
    fi
fi

if [ ${KILL_FLAG} -eq 1 ]; # if the service is currently running, terminate it
then
    if ( pgrep -x 'flask' > /dev/null )
    then
        echo -e ${COLOR}
        echo -n "Terminating running instance of RPHome..."
        echo -e ${NO_COLOR}
        killall -v -9 'flask'
    fi

    if ( pgrep -x 'ngrok' > /dev/null )
    then
        echo -e ${COLOR}
        echo -n "Terminating running instance of ngrok..."
        echo -e ${NO_COLOR}
        killall -v -9 'ngrok'
    fi
fi
