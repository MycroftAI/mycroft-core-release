# mycroft-core-release
A project to automate the mycroft-core release process.
To use:
* Make sure that the user running the script has ssh access to full rights of the core repository in question.
* Set the environment variables for git user and email, the uri of the mycroft-core project, which branch to clone, etc. An example set-env.sh contains the vars.
* Export the variables either in Jenkins, in a script, or in your shell.
* Run `python release.py`
