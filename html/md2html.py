"""md2html
Converts markdown files to html. Can also embed a CSS style.
Requires docopt and markdown2 python libraries.

Usage:
  md2html.py FILE [-s STYLE | --style STYLE] [-o OUTPUT | --out OUTPUT] [-t | --trace] [-i | --inline]
  md2html.py (-h | --help)
  md2html.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -s --style    CSS file to include
  -o --out      File to write to
  -t --trace    Output HTML to console
  -i --inline   Wether to inline the CSS or <link rel="stylesheet">

"""
from docopt import docopt
import markdown2
from os import path

arguments = docopt(__doc__, version='md2html 0.1')
md_source = open(arguments.get("FILE"), 'r').read()
html_source = markdown2.markdown(md_source, extras=[
    "toc",
    "fenced-code-blocks",
    "code-friendly",
    ])
html = "<!DOCTYPE html>\n" + "<html>\n" + "<head>\n"

css_path = arguments.get("STYLE")
if (css_path != None):
    css_source = open(css_path, 'r').read()
    if arguments.get("-i"):
        html = html + "<style>\n" + css_source + "</style>\n\n"
    else:
        html = html + '<link rel="stylesheet" type="text/css" href="' + path.basename(css_path) + '">\n\n'

html = html + "</head>\n" + "<body>\n" + html_source.toc_html + html_source + "</body>\n" + "</html>\n"

out_path = arguments.get("OUTPUT")
if (out_path != None):
    open(out_path, 'w').write(html)

if (arguments.get("--trace")):
    print(html)
