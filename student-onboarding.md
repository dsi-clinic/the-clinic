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

## Meeting & Communication Logistics
TODO
- Which staff are leading the project?
    - Have a project lead and a backup
- Slack
- Weekly team meetings
- Check-in cadence
    - Stand-ups?
- Schedule meetings with external mentors
- Project management
    - TODO: Notion? GitHub issues?
- Troubleshooting SOP
     - Google your error
     - ChatGPT
     - Read the docs for the package you're using
     - Ask (publicly!) in Slack
        - Include error message, operating system, and things you've tried so far
     - Make a reasonable effort to fix your bug (that's how you learn), but don't "stay stuck"

## Hiring
TODO: What is consistent about the hiring process that is worth documenting?
- In-person vs remote policy
    - Are some days/meetings required in person?
    - Do remote days need to be consistent?
    - Communication of in-person/remote schedule
- CPT (Curricular Practical Training) for international students
    - From summer 2023: `If they are current, UC students, no, CPT authorization is not required. Their active F-1 (I-20) and J-1 (DS-2019) are valid for on-campus employment.`
- Graduating students
    - Graduating students need to be hired as "temporary workers." As of summer 2023, this was doable but was an administrative hassle.
- Logging hours
    - TODO: Use Workday?
    - What are the HR gotchas (ie don't log one 15 hour day)

## Summer Programs
TODO
- What does orientation look like and what are orientation expectations?
- Is there an events calendar?
    - What are the expectations and deliverables at the end of the program?
- What is the required check-in cadence for students with the program?
- What is the expected check-in cadence with project mentors?
- Where are students expected to work during the program?
    - What spaces will students have access to?
    - Can students book meeting rooms?
- Will there be "office hours" or some sort of structured troubleshooting time?
    - Who is leading this?
- What is the absence policy?
