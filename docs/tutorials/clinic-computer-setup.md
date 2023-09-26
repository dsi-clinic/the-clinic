# Computer set up for Data Science Clinic

## Intro

This document contains information on how to prepare you computer for the data science clinic. Note that if you do not have these set up properly your grade may be penalized.

Importantly there may be alternatives to the software listed below that has similar functionality. In the case of you using an alternative you will not receive support from the clinic staff/TAs/etc. We _strongly_ recommend you use the options below.

## 1. Unix Command Line Terminal

You need to have access to a command line terminal for many of the tools that are used. If you have a Mac you can find the command line / terminal using the `terminal` application. 

On Windows machines you will need to install _Windows Subsystem for Linux_ ("WSL") and Ubuntu. To do this, follow the instructions [here](https://learn.microsoft.com/en-us/windows/wsl/install). **Importantly** windows has a terminal called PowerShell which _is not_ the same as a unix terminal. If you aren't sure which one you are running, the windows version's prompt will generally looks something like `C:\`.

**Verification:** Make sure that you can open your terminal app and type in the following without getting an error:

    /bin/bash --version


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

Many projects use [make](https://sites.ualberta.ca/dept/chemeng/AIX-43/share/man/info/C/a_doc_lib/aixprggd/genprogc/make.htm) as a way to simplify project development. 

On both Mac and WSL systems with Ubuntu make (should) be installed by default. To verify _check the instructions at the end of this section_.

If not present on WSL/Ubuntu systems you will need to install the `build-essentials` package, which can be done by typing the following at the command prompt or using the Ubuntu installer:

    sudo apt-get install build-essential

On Mac systems, make will also generally be installed, but if it is not then type 

**Verification:** Open your terminal and type in the following command. If it returns without an error than make is installed:

    make --version