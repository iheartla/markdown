"""
Python Markdown

A Python implementation of John Gruber's Markdown.

Documentation: https://python-markdown.github.io/
GitHub: https://github.com/Python-Markdown/markdown/
PyPI: https://pypi.org/project/Markdown/

Started by Manfred Stienstra (http://www.dwerg.net/).
Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
Currently maintained by Waylan Limberg (https://github.com/waylan),
Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

Copyright 2007-2018 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).

PRE-PROCESSORS
=============================================================================

Preprocessors work on source text before we start doing anything too
complicated.
"""

from . import util
from .htmlparser import HTMLExtractor
import re


def build_preprocessors(md, **kwargs):
    """ Build the default set of preprocessors used by Markdown. """
    preprocessors = util.Registry()
    preprocessors.register(NormalizeWhitespace(md), 'normalize_whitespace', 30)
    preprocessors.register(HtmlBlockPreprocessor(md), 'html_block', 20)
    return preprocessors


class Preprocessor(util.Processor):
    """
    Preprocessors are run after the text is broken into lines.

    Each preprocessor implements a "run" method that takes a pointer to a
    list of lines of the document, modifies it as necessary and returns
    either the same pointer or a pointer to a new list.

    Preprocessors must extend markdown.Preprocessor.

    """
    def run(self, lines, **kwargs):
        """
        Each subclass of Preprocessor should override the `run` method, which
        takes the document as a list of strings split by newlines and returns
        the (possibly modified) list of lines.

        """
        pass  # pragma: no cover


class NormalizeWhitespace(Preprocessor):
    """ Normalize whitespace for consistent parsing. """

    def run(self, lines, **kwargs):
        source = '\n'.join(lines)
        source = source.replace(util.STX, "").replace(util.ETX, "")
        source = source.replace("\r\n", "\n").replace("\r", "\n") + "\n\n"
        source = source.expandtabs(self.md.tab_length)
        source = re.sub(r'(?<=\n) +\n', '\n', source)
        return source.split('\n')


class HtmlBlockPreprocessor(Preprocessor):
    """Remove html blocks from the text and store them for later retrieval."""

    def run(self, lines, **kwargs):
        source = '\n'.join(lines)
        parser = HTMLExtractor(self.md)
        parser.feed(source)
        parser.close()
        return ''.join(parser.cleandoc).split('\n')
