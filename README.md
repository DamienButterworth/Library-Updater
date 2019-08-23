# Library-Updater
Tool used to update libraries (minor versions) on Scala projects

Requires at least Python 3.5

### Installation Instructions: 

Either run
`pip install -r requirements.txt` or `pip3 install -r requirements.txt` depending on your default Python version

Install 'Hub':
https://hub.github.com/

Place a [Github Personal Access Token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) with full "repo" access, prefixed with "Bearer" under the environment variable 'GITOAUTH' e.g.:  
`export GITOAUTH="Bearer <Access Token with repo access>"`

### Running the application

#### Library Updater

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

#### Search Repository

Used to search any number of repositories for a particular string

#### Usage

run search_repository.py

#### Questions: 

##### Repository Names (Comma Separated):

A comma separated list of repositories

e.g. bas-gateway, bas-gateway-frontend, ...etc.

##### Search String:

Enter a string you want to find in the projects

e.g. ContinueUrl 

##### In which files?

Enter a string matching the filename desired

e.g. application.conf or .scala


#### Find and Replace

A recursive tool to find all instances of a string in specified files and replace them with a specified string

##### Usage

run find_and_replace.py

"Directory to scan for files?" The directory used to recursively search for strings in files

"Filename e.g. '.txt' or 'SsoConnector.scala:'" the filename specified to search inside for a specified string

"String to replace: " The string you want to replace

"Replace String with: " The string you want to replace with

### Running the tests
`pytest` in repository directory



