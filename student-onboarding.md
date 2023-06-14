This document contains checklists and resources for onboarding students. There are many general onboarding steps that apply to all students (Clinic students, summer program students, RAs) as well as some more sepecific guidelines for each of these types of student engagements.

## Technical Setup
One of the most important first steps is verifying that everyone's tech is working. This can feel like a "slow start" but it pays off to nip technical setup issues in the bud.

- Git & GitHub

    Students often have classroom experience with Git and GitHub, but have not used it in a true "version control" setting.

    Here's a typical flow for getting students going with Git & GitHub:
    - Add students to the GitHub repo. *Protect `main`, `dev`, and any other importantbranches before granting access to the students.*
    - Have the students clone the repo locally using SSH keys (see blow) to auth — not HTTPS or personal access tokens.
    - As a first assignment, have students checkout a branch, add their name to the README file, push the branch to the remote repo, and submit a pull request.
    - This tutorial on Git branching is helpful for familiarizing students with many of the common commands they will use in Git: https://learngitbranching.js.org/?locale=en_US

- SSH Keys

    Generating and authing with SSH keys is one of the more common areas for students to have problems during set up.
    - This tutorial from GitHub does a good job of walking students through the generation of SSH keys and setting them up with their GitHub account: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
    - Students often have messy `.ssh` folders since they've previously created keys, generated keys incorrectly in the past, etc. It can be useful to "start fresh" here.

- VS Code & Python Extension

    If students don't have a strong IDE preference, we recommend VS Code. Most staff use VS Code and can provide support for VS Code issues. If someone is experienced and comfortable with another IDE (PyCharm, Sublime Text, etc.) that's fine.

- Jupyter notebooks

    TODO

- Docker 

    TODO

- WSL

    TODO

- Conda

    TODO

Students are resourceful and will often figure out less than ideal "workarounds" that will come back to bite you/them later. **It's wise to verify that everything is working by literally looking at their computer and checking yourself.**