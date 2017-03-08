# Whitespace

## Setup:
  - Install Docker Toolbox @ https://github.com/docker/toolbox/releases/tag/v1.12.5
  - Check that you have the following installed:
      - docker
      - docker-compose
      - docker-machine
  - Do the following in the terminal:
      - cd to the directory you cloned the repo to
      - type the following commands:
          - docker-machine create --driver virtualbox w-host
          - docker-machine ls
      - note the ip address of w-host
      - type the following commands:
          - eval $(docker-machine env w-host)
          - docker-compose build
          - docker-compose up
      - go to the ip address in your browser
   - Thats it! :) Let me know if you run into any issues
