---
title: "How to run Jupyter interactively from a Slurm node on the DSI cluster"
---

# Why?

Often, we use the DSI cluster to run batch jobs: we submit a procedure, let it run until it finishes, and then look at the results.

Often, we use our own computers (laptops) for interactive work, such as developing a procedure in Jupyter.

Sometimes, we need computing resources that are only available on the DSI cluster, such as specific datasets or the right type of GPU, and we need to work interactively because we're still figuring out what we need to compute. That's what this tutorial is for.

# Overview

This procedure involves three computers: your own (maybe a laptop), the DSI head node, and a Slurm node that you will launch and run Jupyter on. When you type commands in a terminal, it's important to know which computer you're logged into when you run them.

The steps in the procedure are presented here:

<img src="../assets/images/get-jupyter-working.svg" width="100%">

In all of the following, I'll use `> ` as a shell prompt and `ALL-CAPITAL-LETTERS` for text that you need to replace with your own.

# Steps

## Step 1: Log into the DSI head node

This is `fe01`, `fe02`, or `fe03` (your choice), so

```> ssh YOUR-USERNAME@fe01.ds.uchicago.edu```

If you haven't already, make sure that you have a local installation of [Micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#automatic-install) in your home directory. Anything you put in your home directory is accessible to any computer in the cluster, so you can set up the Micromamba files once and for all on the head node. If you need to run a command to enable it (tell Linux that you want to run `python` from your Micromamba installation, instead of the general one), you will need to run that enabling command whenever you log into a new computer in the cluster. (These instructions don't cover Micromamba; that problem can be handled separately.)

## Step 2: Start a Slurm node

Use `srun` (see [Slurm full instructions](https://howto.cs.uchicago.edu/slurm)) like this:

```
> srun -p general --gres=gpu:1 --pty -t 12:00:00 bash
srun: job 523847 queued and waiting for resources
srun: job 523847 has been allocated resources
```

This starts a node requiring a GPU (`--gres=gpu:1`) for 12 hours (`-t 12:00:00`) as an interactive environment that you can log into (`bash`). The time limit is important because it will automatically shut down after the specified length of time (and `-p general` selects the queue that allows more than 10 minutes). If you're done early, shut it down manually with `scancel` to be a good citizen. Also, if you don't need a GPU, don't ask for one—let someone else use it!

## Step 3: Get the name of the Slurm node

The node has started, but it hasn't given you its name so that you can start working. You can get its name from `squeue`:

```
> squeue -u YOUR-USERNAME
```

Here's some sample output:

```
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
            523847   general     bash jpivarsk  R       0:35      1 j001-ds
```

The node is `j001-ds`: it's the one whose `JOBID` matches what `srun` returned. For the rest of this tutorial, I'll call that `YOUR-SLURM-NODE`.

## Step 4: Log into the Slurm node

You do this through an `ssh` command _on the head node_, not on your own computer. As shown in the image above, it's a two-step process.

```
> ssh YOUR-SLURM-NODE
```

You can determine whether you're there by running `hostname`.

## Step 5: Make sure that Micromamba is set up on the Slurm node

If you need to run a command to enable Micromamba (assign its environment variables so that you're using it rather than the base Python), do it now, on the Slurm node. When this is set up properly, `which python` will respond with _your_ installation of Python (a path in your home directory: `/home/YOUR-USERNAME/micromamba/...`). Also be sure that `jupyterlab` is one of the packages you've installed.

## Step 6: Start JupyterLab on the Slurm node

If you're accustomed to starting Jupyter on the command line, you'll need a few additional arguments:

```
> jupyter lab --no-browser --port=8888 --ip=0.0.0.0
```

Since you're running this command on a server on a rack somewhere, you don't want it to try to open a web browser on the server (`--no-browser`) and you should also specify a port (`--port=8888`) and make it world-accessible (`--ip=0.0.0.0`) so that you can open it on a browser on your own computer. JupyterLab will then print a lot of log messages, including a block like

```
    To access the server, open this file in a browser:
        file:///home/jpivarski/.local/share/jupyter/runtime/jpserver-570302-open.html
    Or copy and paste one of these URLs:
        http://j001-ds:8888/lab?token=THE-LONG-STRING-OF-CHARACTERS-THAT-IS-A-PASSWORD
        http://127.0.0.1:8888/lab?token=THE-LONG-STRING-OF-CHARACTERS-THAT-IS-A-PASSWORD
```

You'll want the last URL (containing `127.0.0.1`), but don't try to open it just yet.

## Step 7: Forward Jupyter's port number to your computer

In _another terminal on your own computer_ (see the image above), ssh into the head node again, but this time forward the port from `YOUR-SLURM-NODE` to your computer. This ssh connection just needs to stay open to connect JupyterLab, running on the server, to your own computer, through that port number.

```
> ssh -L 8888:YOUR-SLURM-NODE:8888 YOUR-USERNAME@fe01.ds.uchicago.edu
```

## Step 8: Open Jupyter's URL in your local web browser

Now open the link Jupyter gave you in your own web browser. When it starts up, you should see the files of the remote computer in its file browser, and if you open Jupyter's own web-based terminal, you should be able to verify that it's running on `YOUR-SLURM-NODE` by typing the `hostname` command.

# That's it!

Happy computing!
