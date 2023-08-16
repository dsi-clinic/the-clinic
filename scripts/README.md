### Automated Testing

This directory contains a tool `evaluate_repo` which runs code testing libraries against a repository. 

### How to run

In the root directory run the following commands:

```./build_image.sh```

which will install the image in docker. Make sure that no errors occur.

To run the code on a repository located in `/path-to-repo` execute the following command:

```./run-code-analysis.sh /path-to-repo```

A few important notes:

1. Make sure to `git pull` _before_ running this code.
1. This will get branch information for all branches.
1. This will only run the analysis (`pyflakes` on python files) for the code _in the current branch_. So if you run this while your current branch is `main` it will run on `main`.

If you want to do a full linting, then you can add the argument "LINT" to the `run-code-analysis` command, such as:

```./run-code-analysis.sh /path-to-repo LINT```