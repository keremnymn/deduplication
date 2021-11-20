# How to use?

- First, write your `git log` to a `.log` file.
- Then, run the program using `python main.py 'FULL PATH TO YOUR LOG FILE' ''`

This will create a default `deduplicated.json` in your path.

If you already have a `deduplicated.json` of your own, provide your file as a second command. For example:

`python main.py 'FULL PATH TO YOUR LOG FILE' 'FULL PATH TO YOUR DEDUPLICATED.JSON FILE'`

## "dummygithubaccount"

In order to try the program, I changed the config file as the following:

`git config user.name "Dummy User"`
`git config user.email "dummy@dummy.com"`

locally. And committed some changes using this configuration. But GitHub links this user to an existing and abandoned account, thus it wrongfully shows that `dummygithubaccount` wrote some changes.

###### Developed by Kerem Nayman as a coding challenge. Hope it works!