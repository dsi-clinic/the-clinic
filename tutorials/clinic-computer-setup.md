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

```wsl printf 'Default shell: $0\nUsername: $USER\nHome Directory: $(cd ~ && pwd)'```

This should generate a return of:
```
Default shell: /bin/bash
Username: YOUR_WSL_USERNAME
Home Directory: /home/YOUR_WSL_USERNAME
```
Where `YOUR_WSL_USERNAME` is the username you picked when setting up WSL. It <b>should not be `root`</b> If one of these is incorrect, please go to [troubleshooting instructions](./troubleshooting.md#troubleshooting-wsl)



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

## 6. SSH / AI Cluster

If you need to access the cluster then you will need to request an account (which should have already been done for you). You will then need to set up SSH keys and verify that you can SSH into the machine.

You can find instructions for this process [here](https://github.com/uchicago-dsi/core-facility-docs/blob/main/slurm.md#step-4-enable-authentication-with-ssh-keys). For the purposes of setting up, make sure to get through all of Part 2.

Note that as part of these instructions you will add your SSH key to github. This is a required part of this process.

**Verification:** Open your terminal and type in the following command:

    ssh fe.ds

If you have set this up correctly you should be connected to the AI cluster and see something like `CNET@fe01:~$`. After this, to verify that you have access to the cluster, type in teh following at that prompt:

    srun -p general --pty /bin/bash

If the above command works then you should see something like `CNET@g007:~$` as the prompt. NOTE: you may get the error `srun: error: Lookup failed: Unknown host`, but you can ignore it. If you are NOT properly set up you will see `srun: error: Unable to allocate resources: Invalid account or account/partition combination specified`.

_Make sure to type in `exit` when you are done!_

## 7. SSH / No-AI Cluster

Even if you do not need to access the AI Cluster you will need to authorize command line access. Follow the instructions [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) to complete this step.

Note that you may have completed this step for another class or project. If you aren't sure, test the verification step below.

**Verification:** Open your terminal and type in the following:

    ssh -T git@github.com

If this returns your username and something to the effect of `You've Successfully Authenticated` then it has worked. 