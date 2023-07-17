import os
from utils import is_git_repo
from utils import get_remote_branches_info
from utils import walk_and_process
from utils import parse_arguments

if __name__ == '__main__':
    args = parse_arguments()

    if not os.path.isdir(args.dir_path):
        print(f"Error: {args.dir_path} is not a valid directory.")
        exit(1)

    if not is_git_repo(args.dir_path):
        print(f"Error: {args.dir_path} is not a Git repository.")
        exit(1)

    if os.getenv("LINT") is not None and len(os.getenv("LINT")) > 0:
        lint_flag = True
    else:
        lint_flag = False

    get_remote_branches_info(args.dir_path)
    walk_and_process(args.dir_path, None, lint_flag=lint_flag)
