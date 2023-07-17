import os
from utils import is_git_repo, get_remote_branches_info, walk_and_process, parse_arguments

if __name__ == '__main__':
    args = parse_arguments()

    if not os.path.isdir(args.dir_path):
        print(f"Error: {args.dir_path} is not a valid directory.")
        exit(1)

    if not is_git_repo(args.dir_path):
        print(f"Error: {args.dir_path} is not a Git repository.")
        exit(1)

    get_remote_branches_info(args.dir_path)
    walk_and_process(args.dir_path, args.no_filter)

### EOF ##