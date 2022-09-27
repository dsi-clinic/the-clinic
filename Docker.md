## Docker



### FAQs


#### How does Docker relate to git branches? SSH? What about WSL?

Docker provides a level of abstraction from host operating systems allowing people using different types of operating systems (Windows 11, OS X Mojave, Ubuntu 18.04, Windows 10, etc.) to run the same code in the same way. This can be thought of as a more sophisticated version of conda or venv and a more lightweight version of a virtual machine. A docker container is specified by a `Dockerfile`. One machine may have many containers and they will all be visibile with `docker container ls --all` no matter where you type it. 

Git is used for version control and editing code in teams. Different branches may have different versions of a file so depending on what branch you are on, you may see a different version. If you change branches to one with a new `Dockerfile`, however, this will not change a container that has already been built. To see changes reflected, you will need to rebuild the container. If using VS Code's Remote - Containers extension, it should detect any changes and alert you if you need to rebuild. 

SSH is a protocol for connecting to remote machines. You can `ssh USERNAME@ADDRESS` to connect to the machine at `ADDRESS` as the user `USERNAME`. You may build and connect to Docker containers on remote machines as machines as well

WSL allows Windows users to execute code and programs as if they were using a linux machine. VS Code's 'Remote - WSL' extension allows you to open code files through WSL and handles routing any commands through WSL for you. You can ssh to remote machine or build a container from WSL.

It is possible to connect to WSL, ssh to a remote machine, launch a container there, and connect to that container. It may be very confusing, but this is all just done to ensure when one person runs a python program the same things happens as when their teammate does. 


#### `git push` does not work in Remote - Containers extension

```bash
error: cannot run ssh: No such file or directory
fatal: unable to fork
```
Follow [these instructions](https://code.visualstudio.com/docs/remote/containers#_sharing-git-credentials-with-your-container) from the docs. Note that if you are using WSL2, follow the instructions for Linux, not Windows.

This issue still persists sometimes and is in progress. 

#### Using Docker Compose, getting `Connection Refused` when trying to reach other container

If you are trying to reach a separate container using `localhost`, you should change to the service name in the compose file.


#### I am getting permission denied errors after using Docker


Docker by default runs as a root user. When you make a new file in a container it is owned by root. So outside the container in the repository root, you can `sudo chown -R $USER: .` This will briefly elevate your permissions to root (sudo), and change the ownership (chown) to the current user in the current directory ., and all sub directories recursively (-R).



### Useful Commands

#### Connect to a running container with bash

`docker exec -it CONTAINER_NAME /bin/bash`

#### List all containers

`docker container ls -all`

