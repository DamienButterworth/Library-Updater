# Library-Updater
Tool used to update libraries (minor versions) on Scala projects

Requires at least Python 3.5

### Installation Instructions: 

Either run
`pip install requirements.txt` or `pip3 install requirements.txt` depending on your default Python version

Install 'Hub':
https://hub.github.com/

Place a [Github Personal Access Token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) with full "repo" access, prefixed with "Bearer" under the environment variable 'GITOAUTH' e.g.:  
`export GITOAUTH="Bearer <Access Token with repo access>"`

### Running the application

Branch Name: The name of the branch created by the tool (if requested)  
Commit Message: The message put in the commit (if requested) 

Do you want to automatically push to branch name? (Y/N):  
Y: Auto-pushes to branch with library changes \
N: Attempts to make the changes but will not push the changes

Do you want to automatically raise a pull request? (Y/N):  
Y: Automatically raises a PR with the library changes  
N: Makes the changes but will not create a PR

Do you want to remove the repository after changes? (Y/N):  
Y: Removes the cloned projects at end of execution (recommended if pushing or raising a PR)  
N: Does not removed cloned repositories (recommended for debugging purposes)

### Running the tests
`python run_tests.py` or `python3 run_tests.py`