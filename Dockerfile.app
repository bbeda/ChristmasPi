# base-image for python on any machine using a template variable,
# see more about dockerfile templates here: https://www.balena.io/docs/learn/develop/dockerfile/
FROM balenalib/raspberry-pi2-python:3-stretch-run

# use `install_packages` if you need to install dependencies,
# for instance if you need git, just uncomment the line below.
# RUN install_packages git

# Set our working directory
WORKDIR /usr/src/app

RUN pip3 install gpiozero
RUN pip3 install pigpio

# This will copy all files in our root to the working  directory in the container
COPY . ./
# RUN chmod +x "./startup.sh"

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

# main.py will run when container starts up on the device
#CMD ["/bin/bash","-c","./startup.sh"]
ENTRYPOINT [ "python","-u","src/main.py" ]

