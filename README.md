# What is this?

This Python script deduplicates entries in your `git log` output.

# How to use?

- First, write your `git log` to a `.log` file.
- Then, run the program using `python main.py 'FULL PATH TO YOUR LOG FILE' ''`

This will create a default `deduplicated.json` in your path.

If you already have a `.json` of your own, provide your file as a second command. For example:

`python main.py 'FULL PATH TO YOUR LOG FILE' 'FULL PATH TO YOUR DEDUPLICATED.JSON FILE'`

or else the program will create a default `deduplicated.json` file in the same directory.

###### Developed by Kerem Nayman as a coding challenge.
