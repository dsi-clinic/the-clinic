### Final Cleanup and Technical Review

The purpose of this document is to describe the final code clean up steps to be completed at the end of a data science institute project. This checklist should be considered a set of requirements and while it is possible that some of the items below should not be done, there should be a significant and obvious reason why they are not completed. If a project is not following the below that information needs to be sent to the clinic director and assistant director by email.

These steps are presented in checklist form for ease of evaluation. 

#### General Repo Hygiene
- [ ] Is there only a single branch in the repo containing all work (generally `main`)?
  - Have all, non-main, branches that were created during this project been deleted?
     
#### README 
- [ ] Have all contributors added their names to the appropriate README?
- [ ] Is/are there README file(s) which contain information on how to run the code in the repo, where the data came from and links to all outside information?
- [ ] Is all documentation in markdown format? Are there grammar/syntax/formatting issues which impede comprehension?

#### Code execution
- [ ] Does the README file contain information on how to run the analysis and produce the results?
- [ ] Is there environment information (usually `make`, `docker` or `conda`) specified?

#### Code grading
- [ ] Does the code repository conform to all standards laid out in the [Code Repository Standards document](../coding-standards/coding-standards.md#requirements) in this repo?
- [ ] Please identify three files (making sure to include at least one or two notebooks if there are notebooks in the repo) and evaluate those files for:
  - File names: Is the filename appropriate?
  - Documentation: Is there documentation in a README file describing the contents and purpose of the code in the file?
  - For scripts (*.py files): 
      - Is all code in functions?
      - Do all functions have doc strings?
      - Are function names descriptive?
      - Does black / flake8 pass?
      - Are there any hard-coded paths?
      - Are files referenced appropriate (e.g. no "Nick's Data.csv" or "Nick's Data_v2")?
      - Is there commented out code?
  - For notebooks (*.ipynb files):
      - Are there more than 20 cells?
      - Are there more than 10 lines of code in any cell?
      - Are there `! pip install` lines?
      - Are there function definitions inside the notebook?


