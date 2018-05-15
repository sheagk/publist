TEMPLATES:
article = <myau>, \enquote{<title>.} \textit{<journal>}[ \textbf{<volume>},]{ }...
          [<startpage>--<endpage>|<startpage>|<eid>] (<year>).
book = <au>, \textit{<title>} (<publisher>, <year>).
incollection = <au>, \enquote{<title>,} in \textit{<booktitle>}, [Chap.~<chapter>, ]...
        [pp.~<startpage>--<endpage>|p.~<startpage>|<eid>|] (<publisher>, <year>).
mastersthesis = <au>, \enquote{<title>,} M.S. dissertation (<school>, <year>).
phdthesis = <au>, \enquote{<title>,} Ph.D. dissertation (<school>, <year>).
inproceedings = <myau>, \enquote{<title>} in <booktitle> (<year>)

SPECIAL-TEMPLATES:
authorlist = <author.to_namelist()>
editorlist = <editor.to_namelist()>
au = <authorlist.format_authorlist()>
ed = <editorlist.format_editorlist()>
# sortkey = -[<year>,<month>]
sortkey = [-<eprint>|-<year>]
citelabel = <sortnum>

OPTIONS:
allow_scripts = True         ## whether to allow user scripts in BST files

VARIABLES:
# citelabel = create_citelabel(entry, options)
myau = create_myaulist(entry, options)

DEFINITIONS:
def create_citelabel(entry, options):
    numnames = len(entry['authorlist'])
    if (numnames == 0): return(entry['citenum'])
    foundit = False
    for name in entry['authorlist']:
    	### edit the following to add your own last name
        if ('Kimmel' in name['last']) or ('Garrison' in name['last']):
            foundit = True
            break
    if foundit and False:
        return(r'\textit{' + entry['citenum'] + '}')
    else:
        return(entry['citenum'])

def create_myaulist(entry, options):
    for name in entry['authorlist']:
    	### edit the following to add your own last name
        if ('Kimmel' in name['last']) or ('Garrison' in name['last']):
            for k in name.keys():
                name[k] = r'\textbf{'+name[k]+'}'
    formatted_namelist = format_namelist(entry['authorlist'])
    words = formatted_namelist.split()
    for ii in range(len(words)-1):
        if words[ii] == 'S.' and words[ii+1].startswith(r'\textbf'):
            words[ii] = r'\textbf{S.}'
    toret = ' '.join(words)
    toret = toret.replace(r'}\textit{',r'} \textit{')
    return toret
