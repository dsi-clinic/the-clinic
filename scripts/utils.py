""""
Utility Functions for running automated code and repo reviews.
"""

import os
import json
import argparse
import tempfile
from io import StringIO
from nbconvert import PythonExporter
from termcolor import cprint
import git
from pyflakes.reporter import Reporter
from pyflakes.api import checkPath
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import black
import difflib


def get_current_branch(repo_path):
    """
    Get the name of the current branch in a Git repository.

    Parameters:
        repo_path (str): The path to the Git repository.

    Returns:
        str: The name of the current branch, or None if an error occurs.

    Raises:
        git.InvalidGitRepositoryError: If the repository path is not a valid
        Git repo

        git.GitCommandError: If an error occurs while executing a Git command.
        Exception: For any other unexpected errors.
    """
    try:
        repo = git.Repo(repo_path)
        current_branch = repo.active_branch.name
        return current_branch
    except git.InvalidGitRepositoryError:
        print("Error: Not a valid Git repository.")
    except git.GitCommandError:
        print("Error: Git command error occurred.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def count_functions(cell):
    """Count the number of functions defined in a Jupyter Notebook cell."""
    code = cell["source"]
    return len([1 for line in code if line.strip().startswith("def ")])


def process_notebook(file_path):
    """
    Process a Jupyter Notebook and count the cells, lines of code
    and functions.
    """
    with open(file_path, "r", encoding="utf-8") as f_handle:
        notebook = json.load(f_handle)
        cells = notebook["cells"]
        num_cells = len(cells)
        num_lines = 0
        num_functions = 0
        max_lines_in_cell = 0
        for cell in cells:
            if cell["cell_type"] == "code":

                lines_in_cell = len([1 for line in cell["source"]
                                     if line.strip()])
                num_lines += lines_in_cell
                max_lines_in_cell = max(max_lines_in_cell, lines_in_cell)
                num_functions += count_functions(cell)
        return num_cells, num_lines, num_functions, max_lines_in_cell


def walk_and_process(dir_path, no_filter_flag, lint_flag):
    """Walk through directory and process all Jupyter Notebooks."""

    paths_to_flag = ["__pycache__", "DS_Store", "ipynb_checkpoints"]
    cprint(f"Currently analyzing branch {get_current_branch( dir_path)}",
           color="green")
    pylint_warnings = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)

            pyflake_results = []

            if file.endswith(".ipynb"):
                (
                    num_cells,
                    num_lines,
                    num_functions,
                    max_lines_in_cell,
                ) = process_notebook(file_path)

                if no_filter_flag or (
                    num_cells > 10 or max_lines_in_cell > 15
                        or num_functions > 0
                ):
                    print(f"File: {file_path}")
                    print(f"\tNumber of cells: {num_cells}")
                    print(f"\tLines of code: {num_lines}")
                    print(f"\tNumber of function definitions: {num_functions}")
                    print(f"\tMax lines in a cell: {max_lines_in_cell}")
                    print("-" * 40)

                pyflake_results = pyflakes_notebook(file_path)

            elif file.endswith(".py"):
                pyflake_results = pyflakes_python_file(file_path)
                black_results = black_python_file(file_path)
                if lint_flag:
                    pylint_warnings = get_pylint_warnings(file_path)
                    if len(pylint_warnings) > 0:
                        for warning in pylint_warnings:
                            print(f"{warning}")

                if black_results:
                    print(f"There were {len(black_results)} changes "
                          f"on file {file_path}. Please run black.")
 
            if len(pyflake_results) > 0:
                print(*pyflake_results, sep="\n")

            if len([x for x in paths_to_flag if x in file]) > 0:
                print(f"Warning: the file {file_path} should be \
                      filtered via gitignore.")

    return None


def pyflakes_notebook(path_to_notebook):
    """
    Run pyflakes on a Jupyter notebook.
    :param path_to_notebook: path to the notebook file.
    :return: list of warnings and errors from pyflakes.
    """
    # Convert notebook to Python script
    exporter = PythonExporter()
    script, _ = exporter.from_filename(path_to_notebook)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") \
            as temp:
        temp_name = temp.name
        temp.write(script)

    errors_and_warnings = pyflakes_python_file(temp_name)

    # Delete temporary file
    os.remove(temp_name)
    return errors_and_warnings


def pyflakes_python_file(file_path):
    """
    Run a python file through pyflakes. returns the number of warnings raised.
    """

    # Prepare StringIO object for capturing pyflakes output
    error_stream = StringIO()
    warning_stream = StringIO()

    reporter = Reporter(warning_stream, error_stream)

    # Run pyflakes and capture output
    checkPath(file_path, reporter=reporter)

    # Get errors and warnings
    errors = [
        ":".join([file_path] + x.split(":")[1:])
        for x in error_stream.getvalue().splitlines()
    ]

    warnings = [
        ":".join([file_path] + x.split(":")[1:])
        for x in warning_stream.getvalue().splitlines()
    ]

    return errors + warnings


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process Cod Repository.")
    parser.add_argument(
        "dir_path", type=str, help="Directory path to start the search from"
    )
    return parser.parse_args()


def is_git_repo(repo_path):
    """
    Return a boolean if the directory supplied is a git repo.
    """
    return git.Repo(repo_path).git_dir is not None


def get_remote_branches_info(repo_path):
    """
    This function reutrns the branch information from the
    remote repository.
    """
    repo = git.Repo(repo_path)
    remote_branches = repo.remote().refs

    branch_info = []
    for branch in remote_branches:
        if branch.remote_head == "HEAD":
            continue

        commits_diff = repo.git.rev_list(
            "--left-right", "--count", f"origin/main...{branch.name}"
        )
        num_ahead, num_behind = commits_diff.split("\t")
        branch_info.append([branch.name, num_ahead, num_behind])

    for branch, behind, ahead in branch_info:
        print(f"Branch: {branch}")
        print(f"Commits behind main: {behind}")
        print(f"Commits ahead of main: {ahead}")
        print()

    return branch_info


def get_pylint_warnings(filepath):
    """
    This function (generated by chatgpt) runs pylint on files and r
    eturns all warnings
    """
    pylint_output = StringIO()
    reporter = TextReporter(pylint_output)
    Run([filepath], reporter=reporter, do_exit=False)
    pylint_output.seek(0)
    output_lines = pylint_output.readlines()
    # warnings = [line for line in output_lines if 'warning' in line.lower()]
    warnings = [line.replace("\n", "") for line in output_lines]
    return warnings


def black_python_file(file_path):
    try:
        # Read the content of the file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Use Black's API to format the code
        formatted_content = black.format_file_contents(
            content,
            fast=False,
            mode=black.FileMode(),
        )

        # Compare original and formatted content
        diff = difflib.unified_diff(
            content.splitlines(),
            formatted_content.splitlines(),
            fromfile="original",
            tofile="formatted",
            lineterm="",
        )

        diff_list = list(diff)

        # diff_str = "\n".join(diff)
        return diff_list if len(diff_list) > 0 else None

    except black.NothingChanged:
        return None
    except Exception as e:
        return f"Unexpected error: {e}"
