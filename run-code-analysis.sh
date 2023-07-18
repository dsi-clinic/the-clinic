#!/bin/bash
set -e

if [[ -z "$1" ]]
  then
    echo "### Error: No argument supplied."
    echo "### Please provide the path to the git repo to be tested, such as"
    echo "### ./run-code-analysis.sh /path-to-directory"
    exit -1
fi

echo "Running code analysis on $1"

### Verify directory exists
if [[ ! -d $1 ]]
then
    echo "### Error: Directory $1 does not exist"
    exit -1
fi

echo "$2"
if [[ -z "$2" ]] && [[ "$2" = "LINT" ]]; then
    echo "### Running LINT"
fi 

REPOPATH=`readlink -f $1`
LINT=$2
docker run --platform=linux/amd64 -e "REPOPATH=$REPOPATH" -e "LINT=$LINT" -v $REPOPATH:/container-repo-mount coding-std 
