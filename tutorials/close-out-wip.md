---
title: "Technical Close Out Checklist"
---

Technical Close out checklist

This checklist should be completed and submitted by the date on canvas

1. What branch contains the merged work product from your group from this quarter (aka what branch should we be grading)?
1. The coding standards repository contains a checklist of expectations for your repository. Are there any pieces of this that you did not follow and, if so, why not?

Open question:

If we use docker using a volume mount -- how do we handle the grading with that?

Every repository should have a file called `build-image.sh` which builds your docker container and some of the following:

`run-pipeline-XXX.sh` this runs a specific datapipeline (called `XXX`, where `XXX` should be documented in the code). Note that if you have multiple short data pipelines you are welcome to combine them into one bash script, but if you have multiple longer pipelines each should be there own bash script.

`run-notebook.sh` which should run a jupyter notebook instance (if you have notebooks as part of your deliverables.)

a file called `run-docker.sh` which ``executes`` the repo.

In the case of jupyter notebooks then jupyter should run when I `run-docker.sh`. In the case of a data pipeline, then `run-docker.sh` should start the pipeline. If there are both data pipelines and jupyter notebooks then you should pick whichever one you worked last on as `run-docker.sh`

Grading Process:
1. Read the readme.
1. Run the repo profiler / code assessor:
    * Check output
1. If things break we dig further.