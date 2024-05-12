#!/usr/bin/env python
# coding: utf-8

# In[3]:


import re
from tabulate import tabulate

class SymbolTable:
    def __init__(self):
        self.symbols = []
        self.memory_location_counter = 0

    def add_symbol(self, name, symbol_type, value, line_number):
        memory_location = f"Mem{self.memory_location_counter}"
        self.memory_location_counter += 1
        self.symbols.append([name, symbol_type, value, line_number, memory_location])

    def display_symbol_table(self):
        headers = ["Symbol", "Type", "Value", "Line Number", "Memory Location"]
        print(tabulate(self.symbols, headers=headers, tablefmt="grid"))


def tokenize(code):
    tokens = []
    patterns = {
        'keywords': r'\b(int|float|while|main|if|else|new)\b',
        'identifiers': r'[a-zA-Z_]\w*',
        'literals': r'\d+',
        'operators': r'[-*+/><&&||=]',
        'special_characters': r'[.,\'\[\]{}();:?]'
    }

    regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns.items()))

    line_number = 0
    split_lines = code.split('\n')
    for line in split_lines:
        for match in regex.finditer(line):
            token_type = match.lastgroup
            token = match.group(token_type)
            tokens.append((token, token_type, line_number))
        line_number += 1

    return tokens

def analyze_tokens(tokens, symbol_table):
    for token, token_type, line_number in tokens:
        if token_type == "keywords":
            symbol_type = "keyword"
            value = token
        elif token_type == "identifiers":
            symbol_type = "variable"
            value = token
        elif token_type == "literals":
            symbol_type = "literal"
            value = token
        elif token_type == "operators":
            symbol_type = "operator"
            value = token
        elif token_type == "special_characters":
            symbol_type = "special character"
            value = token
        symbol_table.add_symbol(token, symbol_type, value, line_number)

# Example input code
input_code = """
int x;
void foo() {
    int y;
}
float z;
x = 10;
"""

# Create symbol table instance
symbol_table = SymbolTable()

# Tokenize the input code
tokens = tokenize(input_code)

# Analyze tokens and create symbol table
analyze_tokens(tokens, symbol_table)

# Display the symbol table
symbol_table.display_symbol_table()

