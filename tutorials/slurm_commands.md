
### Important Slurm commands and concepts

1. Run `sinfo` to see what nodes are on the cluster. The first column `PARTITION` will list a `dev` and `general` partition and maybe more. Partitions are just different sets of nodes that different groups of users may have different access to. `TIMELIMIT` is the longest job you can run on a particular partition and `NODES` is the number of nodes in the partition. 
2. Run `squeue` to see the state of the queue. If any jobs are currently running, it will show its JOBID, the PARTITION it is on, what USER owns it, the state of the job (ST column. R = Running, PD = Pending, CG = Completing), and the NODELIST of nodes it is using.
3. To submit a job request, we'll use `srun`. `srun` is for interactive jobs (`sinteractive` is an alias for something similar to this) that allow us to interact with our code while it is attached to the compute node. `srun` has many configurable options, here are the ones we'll use most: 
    - `-t` or time. The duration of the allocation. can be of the format `# of minutes:# of seconds` so `-t 240:00` would request a node for 240 minutes. 
    - `--mem` or memory. The amount of memory/RAM you would like. By default a number is read in KBs, but by ending with G it is read in GBs. So `--mem 1000` would request 1000 KBs and `--mem 16G` would request 16 gigabytes. 
    - `-p` or partition. Use `general` for interactive jobs. 
    - `--gres` or 'generic resources' is what we use to request gpus. `--gres=gpu:1` will request a single gpu. 
    - `--pty` is added to attach to the process in a pseudoterminal. 
4. Run `srun -p general -t 5:00 --mem 1G --pty /bin/bash` to request a compute node. 
5. Now your terminal is connected to the compute node. Notice that `ls` and `pwd` give the same results as before. This is because the compute nodes and login nodes use the same filesystems. If you edit a file in one, the second it is saved it will be visible in the other. Type `exit` to end your job and return to a login node. You can also cancel a job by running `scancel JOB_ID`. 