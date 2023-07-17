import os
import json
import git
import argparse
import pyflakes.api

def count_functions(cell):
    """Count the number of functions defined in a Jupyter Notebook cell."""
    code = cell['source']
    return sum([1 for line in code if line.strip().startswith('def ')])

def process_notebook(file_path):
    """Process a Jupyter Notebook and count the cells, lines of code and functions."""
    with open(file_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
        cells = notebook['cells']
        num_cells = len(cells)
        num_lines = 0
        num_functions = 0
        max_lines_in_cell = 0
        for cell in cells:
            if cell['cell_type'] == 'code':
                lines_in_cell = sum([1 for line in cell['source'] if line.strip()])
                num_lines += lines_in_cell
                max_lines_in_cell = max(max_lines_in_cell, lines_in_cell)
                num_functions += count_functions(cell)
        return num_cells, num_lines, num_functions, max_lines_in_cell

def walk_and_process(dir_path, no_filter_flag):
    """Walk through directory and process all Jupyter Notebooks."""
    notebook_count = 0
    stats_printed = 0
    python_file_count = 0

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith('.ipynb'):
                notebook_count += 1                
                num_cells, num_lines, num_functions, max_lines_in_cell = process_notebook(file_path)
                if no_filter_flag or (num_cells > 10 or max_lines_in_cell > 15 or num_functions >0 ): 
                    stats_printed += 1
                    print(f'File: {file_path}')
                    print(f'\tNumber of cells: {num_cells}')
                    print(f'\tLines of code: {num_lines}')
                    print(f'\tNumber of function definitions: {num_functions}')
                    print(f'\tMax lines in a cell: {max_lines_in_cell}')
                    print('-' * 40)
            elif file.endswith('.py'):
                python_file_count += 1
                number_of_messages = run_pyflakes_file(file_path)
                if number_of_messages > 0: 
                    stats_printed += 1

    print(f"Files information printed: {stats_printed}")

def run_pyflakes_file(file_path):
    """Run a python file through pyflakes. returns the number of warnings raised."""

    with open(file_path, "r") as file:
        file_content = file.read()
        number_of_warnings = pyflakes.api.check(file_content, file_path)

    return number_of_warnings

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process Jupyter Notebooks.')
    parser.add_argument('dir_path', type=str, help='Directory path to start the search from')
    parser.add_argument('--no_filter', action='store_true', help='Print stats on all files')
    return parser.parse_args()

def is_git_repo(repo_path):
    return git.Repo(repo_path).git_dir is not None

def get_remote_branches_info(repo_path):
    repo = git.Repo(repo_path)
    remote_branches = repo.remote().refs

    branch_info = []
    for branch in remote_branches:
        if branch.remote_head == "HEAD":
            continue

        commits_diff = repo.git.rev_list('--left-right', '--count', f'origin/main...{branch.name}')
        num_ahead, num_behind = commits_diff.split('\t')
        branch_info.append( [branch.name, num_ahead, num_behind])
        
    for branch, behind, ahead in branch_info:
        print(f"Branch: {branch}")
        print(f"Commits behind main: {behind}")
        print(f"Commits ahead of main: {ahead}")
        print()

    return branch_info