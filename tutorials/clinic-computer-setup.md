---
title: "Computer Setup for Data Science Clinic"
---

# Computer set up for Data Science Clinic

## Intro

This document contains information on how to prepare you computer for the data science clinic. Note that if you do not have these set up properly your grade may be penalized.

Importantly there may be alternatives to the software listed below that has similar functionality. In the case of you using an alternative you will not receive support from the clinic staff/TAs/etc. We _strongly_ recommend you use the options below.

## 1. Unix Command Line Terminal

You need to have access to a command line terminal for many of the tools that are used. If you have a Mac you can find the command line / terminal using the `terminal` application. 

On Windows machines you will need to install _Windows Subsystem for Linux_ ("WSL") and Ubuntu. To do this, follow the instructions [here](https://learn.microsoft.com/en-us/windows/wsl/install). **Importantly** windows has a terminal called PowerShell which _is not_ the same as a unix terminal. If you aren't sure which one you are running, the windows version's prompt will generally looks something like `C:\`.

**Verification:** Make sure that you can open your terminal app and type in the following without getting an error:

    /bin/bash --version

**Additional Windows Verification:** Make sure that you can complete the above _and_ open PowerShell in your terminal app and run:

    wsl printf 'Default shell: $0\nUsername: $USER\nHome Directory: $(cd ~ && pwd)'

This should generate a return of:

    Default shell: /bin/bash
    Username: YOUR_WSL_USERNAME
    Home Directory: /home/YOUR_WSL_USERNAME

Where `YOUR_WSL_USERNAME` is the username you picked when setting up WSL. It <b>should not be `root`</b> If one of these is incorrect, please go to [troubleshooting instructions](./troubleshooting.md#troubleshooting-wsl)

Additionally, open File Explorer, scroll to the bottom left, select 'Linux', 'Ubuntu', 'home', then right click on your username and select 'Pin to Quick Access'. Now your ubuntu home directory should appear in the top/middle left of file explorer.


## 2. Visual Studio Code

Our default IDE is Visual Studio Code. For both PC and Macs you need to follow the link [here](https://code.visualstudio.com/download). 

**Verification:** Make sure that you can open Visual Studio Code and can open and save a file.

## 3. Terminal based git

We expect students to have access to command line / terminal versions of git. While there are visual ways to access git (such as TortoiseGit, etc.) we expect git to be available on the command line when debugging issues. 

More information on git can be found [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Note that git (probably) will not need to be installed as it is frequently installed as part of another package.

**Verification:** Make sure that you can open your terminal app and type in the following without getting an error:

    git --version

## 4. Docker

On Mac you should install [docker desktop](https://docs.docker.com/desktop/) which is relatively straightforward to install. 

On Windows you will need to follow the instructions [here](https://docs.docker.com/desktop/windows/wsl/) for how to install docker on WSL.

**Verification:** Open up your terminal and type in the following command. If it returns without an error then Docker is installed.

    docker --version


## 5. Make

Many projects use [make](https://www.gnu.org/software/make/manual/make.html) as a way to simplify project development. 

On both Mac and WSL systems with Ubuntu make (should) be installed by default. To verify _check the instructions at the end of this section_.

If not present on WSL/Ubuntu systems you will need to install the `build-essentials` package, which can be done by typing the following at the command prompt or using the Ubuntu installer:

    sudo apt-get install build-essential

On Mac systems, make will also generally be installed, but if it is not then type 

**Verification:** Open your terminal and type in the following command. If it returns without an error than make is installed:

    make --version

## 6. SSH Keys

We will use SSH keys to authenticate to github and (if applicable) the DSI Cluster. Please see [these instructions](./ssh_github_cluster.md). 

**Verification:** Open your terminal and type the following command:

    ssh -T git@github.com

If this returns your username and something to the effect of `You've Successfully Authenticated` then it has worked. 

## 7. DSI Cluster

If you need to access the cluster then you will need to request an account (which should have already been done for you). You will then need to set up SSH keys and verify that you can SSH into the machine. Note that the step-by-step instructions for how to do this are included in the [same SSH Keys docs as in section 6](./ssh_github_cluster.md). 

Note that as part of these instructions you will add your SSH key to github. This is a required part of this process.

**Verification:** Open your terminal and type in the following command:

    ssh fe.ds

If you have set this up correctly you should be connected to the AI cluster and see something like `CNET@fe01:~$`. After this, verify you set up ssh keys correctly:

    ssh-add -l
    ssh -T git@github.com

These commands should return something like `256 SHA256:sdlfjkwljflsdfkjs;flkjs;lfj user@host (ED25519)` and `Hi USERNAME! You've successfully authenticated ...`


After this, to verify that you have access to the cluster, type in the following at that prompt:

    srun -p general --pty /bin/bash

If the above command works then you should see something like `CNET@g007:~$` as the prompt. NOTE: you may get the error `srun: error: Lookup failed: Unknown host`, but you can ignore it. If you are NOT properly set up you will see `srun: error: Unable to allocate resources: Invalid account or account/partition combination specified`.

_Make sure to type in `exit` when you are done!_

## 8. GitHub Repository Cloned

You should have your GitHub repository cloned to the correct location(s).

**Verification:** Open your GitHub repository in VS Code. 
- If your project uses a devcontainer for Docker, it should be in the devcontainer extension. 
- If you use Windows, your project should be located in the WSL filesystem.
- If you are using the cluster, your repository should be cloned on the cluster. 
