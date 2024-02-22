### Final Cleanup and Technical Review

The purpose of this document is to describe the final code clean up steps to be completed at the end of a Data Science Institute project. This checklist should be considered a set of requirements and while it is possible that some of the items below should not be done, there should be a significant and obvious reason why they are not completed. If a project is not following the below that information needs to be sent to the clinic director and assistant director by email.

While we want all code to follow the [Code Repository Standards document](../coding-standards/coding-standards.md#requirements), we use the checklist below to focus on specific files which we will grade.

## Students

For each repository associated with your work, a TA will be grading the repository. There are repository wide grading standards as well as specific file grading. TAs will be provided three python or jupyter notebooks from your repository that have commits from this last quarter (the clinic director will look at the git history of files that were changed during this time to select the files).

Those three files will be opened, verified and evaluated against the rubric below.

## Grading Rubric

For TAs, please fill out the following form (one per repository):

| Project Name | | 
| --- | --- | 
| TA Name | | 
| Repo Location (url) | | 
| Three files graded (full path) | <ul><li>File 1</li><li>File 2</li><li>File 3</li></ul>| 

For each of the items below, please fill in the checkmark [X] if it is satisfied. Leave the checkmark blank [ ] if it is not.



#### General Repo Hygiene
- [ ] All work has been merged to the `dev` or `main` branch and other branches have been deleted.
- [ ] There are no `DS_Store` files or `.ipynb_checkpoints` directories.
     
#### Documentation 
- [ ] The repo has a main README.md file which contains information on how to run the code in the repo, where the data came from and links to all outside information.
- [ ] All contributors have added their names to the main README.md file.
- [ ] All documentation is in markdown format.
- [ ] The repository is easy to read and there are no grammar/syntax/formatting issues which impede comprehension.
- [ ] There are descriptions of all files and their purpose in the README.
- [ ] All data has a description and source. This may be in a separate file in a `/data` directory or the main README.
- [ ] Environment information (usually `make`, `docker` or `conda`) is specified.

#### Code grading
Please identify three random files edited by students during the last quarter (making sure to include at least _one_ or _two_ notebooks if there are notebooks in the repo) and evaluate those files for the following. Please specify which three files you choose in the form above.

- [ ] File names: Files should be named appropriately.
- [ ] Is this a script (*.py files)?: 
    - [ ] All code is in functions.
    - [ ] All functions have doc strings.
    - [ ] Function names are descriptive.
    - [ ] `black` and `flake8` pass.
    - [ ] All paths are relative (no hard-coded paths).
    - [ ] Comments are human readable and descriptive (there is no commented-out code or commented out code blocks).
    - [ ] Code is free of API Keys or secrets.
- [ ] Is this a notebook (*.ipynb file)?:
    - [ ] There are less than 20 cells.
    - [ ] Every cell has less than 10 lines of code.
    - [ ] Code is free of environment management (no `! pip install` / `! conda install` lines).
    - [ ] All functions are defined in helper files (there are no `def` or `class` in notebooks).
    - [ ] Comments are human readable and descriptive (there is no commented-out code or commented out code blocks).
    - [ ] Code is free of API Keys or secrets.
