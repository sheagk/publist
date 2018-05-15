#!/usr/bin/env python

"""
Shea Garrison-Kimmel, Sep 26, 2017
sheagk@gmail.com
"""


import sys
import urllib.request

# Fix Python 2.x.
try: input = raw_input
except NameError: pass

usage = "usage:  python {0} <input .bib file> <output file>".format(sys.argv[0].split('/')[-1])
try:
    fname,outname = sys.argv[1],sys.argv[2]
except IndexError:
    print(usage)
    sys.exit(1)

try:
    import  bibtexparser,textwrap
    from pylatexenc.latex2text import LatexNodes2Text #,bibulous
except ImportError:
    print("Require bibtexparser, textwrap and pylatexenc.  Install them with pip")
    sys.exit(1)

with open(fname,'r') as f:
    database = bibtexparser.load(f)

first_author = []
nth_author = []
proceedings = []

for entry in database.entries:
    if 'journal' not in entry.keys():
        proceedings.append(entry)
        continue
    aulist = entry['author'].split('and')
    if 'Garrison' in aulist[0] or 'Kimmel' in aulist[0]:
        first_author.append(entry)
    elif 'Garrison' in entry['author'] or 'Kimmel' in entry['author']:
        nth_author.append(entry)
    else:
        print("uh oh!  Didn't find myself in {}+{}:  {}!".format(aulist[0], entry['year'], entry['title']))


#Ok, now I need to turn the dictionaries into my formatted entries, with proper html styling.

#a proper entry will look like, in html:
# <li>
#     <a href="http://adsabs.harvard.edu/abs/2017arXiv170103792G"><b>Not so lumpy after all: modeling the depletion of dark matter subhalos by Milky Way-like galaxies</b></a><br />
#     S. Garrison-Kimmel, A. Wetzel, J. Bullock, P. Hopkins, M. Boylan-Kolchin, C.-A. Faucher-Gigu&egrave;re, D. Kere&scaron;, E. Quataert, R. Sanderson, A. Graus, T. Kelley, submitted to <i>MNRAS</i>
# </li>

# #or, for an accepted paper:
# <li>
#     <a href="http://adsabs.harvard.edu/abs/2017MNRAS.464.3108G"><b>Organized Chaos: Scatter in the relation between stellar mass and halo mass in small galaxies</b></a><br />
#     S. Garrison-Kimmel, J. Bullock, M. Boylan-Kolchin, E. Bardwell (2017), <i>MNRAS</i>,464,3108
# </li>

#LatexNodes2Text().latex_to_text("{O{\\~n}orbe}").encode('ascii', 'xmlcharrefreplace')
#or
#from BeautifulSoup import BeautifulStoneSoup
# import cgi

# def HTMLEntitiesToUnicode(text):
#     """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
#     text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
#     return text

# def unicodeToHTMLEntities(text):
#     """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
#     text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
#     return text


print("Have {} first author papers and {} nth author papers".format(len(first_author),len(nth_author)))


options = {}
options['use_firstname_initials'] = True
options['maxauthors'] = 10
options['etal_message'] = 'et al.'


def format_aulist(aulist,options):
    austring = ""
    cut = False
    if len(aulist) > options['maxauthors']:
        aulist = aulist[:options['maxauthors']]
        cut = True
        andstring = ' '
    else:
        andstring = 'and '
    for au in aulist:
        first = au.split(',')[-1].strip()
        first = first.replace('~',' ')
        last = au.split(',')[0].strip()
        # last = last.lstrip('{')
        # last = last.rstrip('}')
        last = last[1:-1]
        if au == aulist[-1]:
            austring += andstring
        austring += first +' '+ last + ', '
    if cut:
        austring += options['etal_message']
    else:
        austring = austring[:-2]
    return austring.replace('-\n', '-').replace('\n', ' ')



def latex_to_html(string):
    #have to strip off b' and '
    return str(LatexNodes2Text().latex_to_text(string).encode('ascii', 'xmlcharrefreplace'))[2:-1]

def astrojournals(journal):
    #just the most common ones I care about
    replace = {
                'aj':'AJ',
                'araa':'ARA&A',
                'apj':'ApJ',
                'apjl':'ApJ Letters',
                'apjs':'ApJS',
                'ao':'Appl. Opt.',
                'apss':'Ap&SS',
                'aap':'A&A',                # Astronomy and Astrophysics
                'aapr':'A&A Rev.',          # Astronomy and Astrophysics Reviews
                'aaps':'A&AS',              # Astronomy and Astrophysics, Supplement
                'azh':'AZh',                 # Astronomicheskii Zhurnal
                'baas':'BAAS',               # Bulletin of the AAS
                'jrasc':'JRASC',             # Journal of the RAS of Canada
                'memras':'MmRAS',            # Memoirs of the RAS
                'mnras':'MNRAS',             # Monthly Notices of the RAS
                'pra':'Phys. Rev. A',        # Physical Review A: General Physics
                'prb':'Phys. Rev. B',        # Physical Review B: Solid State
                'prc':'Phys. Rev. C',        # Physical Review C
                'prd':'Phys. Rev. D',        # Physical Review D
                'pre':'Phys. Rev. E',        # Physical Review E
                'prl':'Phys. Rev. Lett.',    # Physical Review Letters
                'pasp':'PASP',               # Publications of the ASP
                'pasj':'PASJ',               # Publications of the ASJ
                'qjras':'QJRAS',             # Quarterly Journal of the RAS
                'skytel':r'S\&T',             # Sky and Telescope
                'solphys':'Sol. Phys.',      # Solar Physics
                'sovast':'Soviet Ast.',      # Soviet Astronomy
                'ssr':'Space Sci. Rev.',     # Space Science Reviews
                'zap':'ZAp',                 # Zeitschrift fuer Astrophysik
                'nat':'Nature',              # Nature
                'iaucirc':'IAU Circ.',       # IAU Cirulars
                'aplett':'Astrophys. Lett.', # Astrophysics Letters
                }
    if journal in replace:
        return replace[journal]
    elif journal[1:] in replace:
        return replace[journal[1:]]
    else:
        return journal

journalopts = {'0':'MNRAS','1':'ApJ','2':'MNRAS Letters','3':'ApJ Letters'}
jostring = ""
for k in sorted(journalopts.keys()):
    jostring += '\t'+k+':  '+journalopts[k]
    if k == '0':
        jostring += ' (default)\n'
    else:
        jostring += '\n'
def process_entries(entry_list):
    string = ""
    for entry in entry_list:
        title = entry['title'].replace('-\n','-').replace('\n', ' ')
        aulist = entry['author'].split(' and')
        austring = format_aulist(aulist,options=options)
        # if 'umpy' in title:
        #     print entry['aulist'],aulist,austring
        url = entry['adsurl']
        journal = entry['journal']
        if 'ArXiv' in journal:
            try:
                #try to figure it out from the website data; fall back to asking if we fail
                eprint = entry['eprint']
                url = 'https://arxiv.org/abs/'+eprint
                with urllib.request.urlopen(url) as response:
                    arxiv_website = str(response.read())
                idx = arxiv_website.lower().find('submitted to')
                if idx <= 0:
                    raise KeyError("Can't find journal in arXiv text")
                idx += len('submitted to ')
                journal = arxiv_website[idx:].strip().split('</')[0].split()[0].strip().strip(';,.\n')
                # print(entry['title'], journal)
            except Exception as e:
                printstring = textwrap.fill(title,initial_indent='    ', subsequent_indent='    ')
                journal = input('Failed to get journal for\n'+printstring+'\nautomatically.  What was it submitted to?\n'+jostring)
                if journal in journalopts.keys():
                    journal = journalopts[journal]
                elif journal == '':
                    journal = journalopts['0']
            journal = 'submitted to <i>'+journal+'</i>'
            year = ''
            volume = ''
            pages = ''
        else:
            journal = r'<i>'+astrojournals(journal)+r'</i>, '
            year = ' ('+entry['year']+')'
            if 'volume' in entry:
                volume = entry['volume']+', '
                pages = entry['pages']
            else:
                #must be in press
                volume = 'in press'
                pages = ''

        string += r'<li>'+'\n\t'
        string += r'<a href="'+url+'"><b>'+latex_to_html(title)+r'</b></a><br />'+'\n\t'
        string += latex_to_html(austring)+year+', '+journal+volume+pages+'\n'
        string += r'</li>'+'\n\n'
    return string


first_author_string = process_entries(first_author)
nth_author_string = process_entries(nth_author)

out = open(outname,'w')
out.write(r'<!-- First author publications -->'+'\n\n'+first_author_string+'\n\n\n'+r'<!-- Nth author publications -->'+'\n\n'+nth_author_string)












