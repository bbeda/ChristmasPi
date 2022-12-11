function handle_terminate(){
    echo "kill pigpiod"
    killall pigpiod
}

sudo pigpiod

trap handle_terminate SIGKILL 
trap handle_terminate SIGTERM

read