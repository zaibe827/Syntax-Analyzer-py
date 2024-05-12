#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
   int main() {
        float pi = 3.14;
        int radius = 5;
        float area = pi * radius * radius;
        printf("The area of the circle is %f\n", area);
        return 0;
    }
"""

# Create symbol table instance
symbol_table = SymbolTable()

# Tokenize the input code
tokens = tokenize(input_code)

# Analyze tokens and create symbol table
analyze_tokens(tokens, symbol_table)

# Display the symbol table
symbol_table.display_symbol_table()

class LexicalAnalyzer:
    def __init__(self, buffer_size=50):
        self.keywords = {"int", "float", "printf", "double", "char"}
        self.operators = {"+", "-", "*", "/", "=", "<", ">", "!", "&", "|"}
        self.special_characters = {"(", ")", "{", "}", ";", ","}
        self.string_literals = set()
        self.variables = set()
        self.constants = set()
        self.buffer_size = buffer_size
        self.input_buffer1 = ''
        self.input_buffer2 = ''
        self.current_buffer = self.input_buffer1
        self.in_string = False  # Flag to track if we are currently inside a string literal 

    def analyze_input(self, input_text):
        for char in input_text:
            if self.in_string:
                self.current_buffer += char
                if char == '"':  # If we encounter the ending double quote
                    self.process_token(self.current_buffer)
                    self.current_buffer = self.switch_buffer(self.current_buffer)
                    self.in_string = False
            else:
                if char in {' ', '\n', '(', ')', '{', '}', ';', ','}:
                    if self.current_buffer.strip():  # Check if current_buffer is not just whitespace
                        self.process_token(self.current_buffer.strip())
                    self.current_buffer = self.switch_buffer(self.current_buffer)
                elif char in {'+', '-', '*', '/', '=', '<', '>', '!', '&', '|'}:
                    if self.current_buffer.strip():
                        self.process_token(self.current_buffer.strip())
                    print(f"Operator: {char}")
                    self.current_buffer = self.switch_buffer(self.current_buffer)
                elif char == '"':
                    self.in_string = True
                    self.current_buffer += '"'
                else:
                    self.current_buffer += char

            if len(self.current_buffer) >= self.buffer_size:
                self.current_buffer = self.switch_buffer(self.current_buffer)

        if self.current_buffer:
            self.process_token(self.current_buffer)

    def process_token(self, token):
        if token in self.keywords:
            print(f"Keyword: {token}")
        elif token in self.special_characters:
            print(f"Special Character: {token}")
        elif re.match(r'^[+-]?\d*(?:\.\d*)?$', token):
            print(f"Constant: {token}")
            self.constants.add(token)
        elif token.startswith('"') and token.endswith('"'):
            print(f"String Literal: {token}")
            self.string_literals.add(token)
        else:
            print(f"Variable: {token}")
            self.variables.add(token)

    def switch_buffer(self, current_buffer):
        if current_buffer is self.input_buffer1:
            return self.input_buffer2
        else:
            return self.input_buffer1
if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    input_text = """
    int main() {
        float pi = 3.14;
        int radius = 5;
        float area = pi * radius * radius;
        printf("The area of the circle is %f\n", area);
        return 0;
    }
    """
    analyzer.analyze_input(input_text)
    
# Define the symbol table
symbol_table = {}


