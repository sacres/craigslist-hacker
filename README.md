craigslist-hacker
=================

Forked from: https://github.com/brandonhsiao/craigslist-hacker

This version of craigslist-hacker searches Craigslist for sysadmin/devops roles (under
/sad/). First:

    python main.py --init

to build the list of craigslist subsites that are worth checking (the
ones that regularly have jobs). This takes a fair amount of time
depending on your internet connection. You only need to do this once.
To search jobs:

    python main.py --search

which stores everything into `post.html`.
