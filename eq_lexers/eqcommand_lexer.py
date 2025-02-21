import re
from pygments.lexer import RegexLexer, bygroups
from pygments.token import *

class EQCommandLexer(RegexLexer):
    name = 'EverQuest Command Syntax'
    aliases = ['eqcommand']
    flags = re.MULTILINE  # enable multiline so '^' matches the start of each line

    tokens = {
        # the /command
        'root': [
            (r'^/[\w-]+', Name.Tag),  # Command name
            (r'\s+', Text),
            (r'\.{3}', Punctuation),  # Ellipsis
            (r'\{', Punctuation, 'curly'),
            (r'\[', Punctuation, 'square'),
            (r'<', Punctuation, 'angle_required'),  # Use required version in root
            (r'\|', Punctuation),
            (r'[^\s<\[\{\|]+', Name.Constant),  # Required items in root (same as curly)
        ],
        # things in curly brackets
        'curly': [
            (r'\}', Punctuation, '#pop'),
            (r'\|', Punctuation),
            (r'\s+', Text),
            (r'<', Punctuation, 'angle_required'),  # Use required version in curly
            (r'\[', Punctuation, 'square'),
            (r'\{', Punctuation, 'curly'),
            (r'[^}\|<\[\{\s]+', Name.Constant),
        ],
        # things in square brackets
        'square': [
            (r'\]', Punctuation, '#pop'),
            (r'\|', Punctuation),
            (r'\s+', Text),
            (r'<', Punctuation, 'angle_optional'),  # Use optional version in square
            (r'\[', Punctuation, 'square'),
            (r'\{', Punctuation, 'curly'),
            (r'[^\]<\|\{\[\s]+', Name.Label),
        ],
        # Angle brackets in required context (root/curly)
        'angle_required': [
            (r'>', Punctuation, '#pop'),
            (r'"[^"]+"', Name.Variable.Required),           # Use Name for required placeholders
            (r'[^>]+', Name.Variable.Required),             # Use Name for required placeholders
        ],
        # Angle brackets in optional context (square)
        'angle_optional': [
            (r'>', Punctuation, '#pop'),
            (r'"[^"]+"', Name.Variable),  # Keep Name.Variable for optional placeholders
            (r'[^>]+', Name.Variable),    # Keep Name.Variable for optional placeholders
        ],
    }