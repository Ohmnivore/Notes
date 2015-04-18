"""md2html
Converts markdown files to html. Can also embed a CSS style.
Requires docopt and markdown2 python libraries.

Usage:
  md2html.py FILE [-s STYLE | --style STYLE] [-o OUTPUT | --out OUTPUT] [-t | --trace]
  md2html.py (-h | --help)
  md2html.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -s --style    CSS file to include
  -o --out      File to write to
  -t --trace    Output HTML to console

"""
from docopt import docopt
import markdown2

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
    html = html + "<style>\n" + css_source + "</style>\n\n"

html = html + "</head>\n" + "<body>\n" + html_source.toc_html + html_source + "</body>\n" + "</html>\n"

out_path = arguments.get("OUTPUT")
if (out_path != None):
    open(out_path, 'w').write(html)

if (arguments.get("--trace")):
    print(html)
