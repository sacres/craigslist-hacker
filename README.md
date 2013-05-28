craigslist-hacker
=================

craigslist-hacker searches Craigslist for programming jobs (under
/cpg/). First:

    python main.py --init

to build the list of craigslist subsites that are worth checking (the
ones that regularly have jobs). This takes a fair amount of time
depending on your internet connection. You only need to do this once.
To search jobs:

    python main.py -search

which stores everything into `post.html`.
