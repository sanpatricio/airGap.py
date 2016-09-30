# nomiGrate
## version 0.9
By Patrick Riggs (github: sanpatricio)

nomiGrate assists you with nominating for migration (get it?) files that may be ready for copying between two air-gapped systems or networks by recursively looking through a directory for files modified within N days ago, then offering a couple ways to proceed with the list of nomiGrated files (display on screen, write to log file, copy itentified files to a directory)

Example session:

```
me@handoftheking $ ./nomiGrate.py 
In which directory do I begin my search: ./testing
How many days back am I looking: 1
Searching for files modified since 2016-09-29 21:04:48.908844
Found 1 modified files in the last 1 day(s).
Actions:
[1] Nothing, return to command line.
[2] Collect copies of his in ./20160930-210448-nominatedForMigration/
[3] Write these results to ./20160930-210448-nomiGrate-Report.txt
[4] Write these results to the screen
What should I do with them [1]: 4
2016-09-30 19:30:./testing/file.txt
```
