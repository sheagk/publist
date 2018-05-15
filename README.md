# publist
A few tools for automating lists of publications, both for your CV and your website.  The idea is that you should be able to update your publication list just via bibtex.  This turns out to be easier for html than for the CV, but is doable for both with a lot less work than manually updating every time you put out a new paper.

The basic idea is that you should export a bibtex file (e.g. from https://ui.adsabs.harvard.edu/) that contains all your publications (first or Nth author).  Then you can update that bibtex file, add new entries to the appropriate place in your CV tex file, run a couple commands, and you're done.

* bib_to_html.py -- Script to convert a bibtex file into an HTML list of first-author and Nth author publications, for the purposes of copy/pasting into a website.
  * Requirements:
    * bibtexparse
    * textwrap
    * pylatexenc

* cvtools
  * cv_template.tex -- template for the publication list section of your CV
  * compile -- bash script to compile the CV
  * bibstyle.bst -- bibulous bibliography formatting file.  Includes two lines that need to be changed to pick out your own name.
  
  * Requirements:
    * bibulous
      * currently set up assuming a valid python3 module.  edit ``compile`` to use a different call to bibulous (e.g. if you're using python2).  I recommend using my forked version available at https://github.com/sheagk/bibulous, which should be python3 compatible.
