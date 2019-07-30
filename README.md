# Library-Updater
Tool used to update libraries (minor versions) on Scala projects

Installation Instructions: 

Install 'Hub':
https://hub.github.com/

Place an OAUTH Token under the environment 'GITOAUTH' or point the code to an OAUTH Token on line:
https://github.com/DamienButterworth/Library-Updater/blob/a01d6590caf6d11496b26f6b9ae9b5072f0465f4/latest_hmrc_release.py#L9

Run the application

Branch Name: The name of the branch created by the tool (if requested) \
Commit Message: The message put in the commit (if requested) \

Do you want to automatically push to branch name? (Y/N): \
Y: Auto-pushes to branch with library changes \
N: Attempts to make the changes but will not push the changes

Do you want to automatically raise a pull request? (Y/N): \
Y: Automatically raises a PR with the library changes \
N: Makes the changes but will not create a PR
