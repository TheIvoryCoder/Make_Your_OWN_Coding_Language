import regex as re

def lexer(contents):
    lines = contents.split('\n')

    nLines = []
    for line in lines:
        chars = list(line)
        temp_str = ""
        tokens = []
        quote_count = 0
        for char in chars:
            if char == '"' or char == "'":
                quote_count += 1
            if quote_count % 2 == 0:
                in_quotes = False
            else:
                in_quotes = True
            if char == " " and in_quotes == False:
                tokens.append(temp_str)
                temp_str = ""
            else:
                temp_str += char
        tokens.append(temp_str)
        items = []
        for token in tokens:
            if token[0] == "'" or token[0] == '"':
                if token[-1] == '"' or token[-1] == "'":
                    items.append(("string", token))
                else:
                    # Throw Error
                    break
            elif re.match(r"[.a-zA-Z]+", token):
                items.append(("symbol", token))
            elif token in "+-*/":
                items.append(("expression", token))
            elif re.match(r"[.0-9]+", token):
                items.append(("number", token))
        nLines.append(items)
    return nLines

Symbols = [
    "var",
    "function"
]

Vars = {
    
}

# Vars["x"] = "Hello world!"
def parse(file):
    contents = open(file, 'r').read()
    lines = lexer(contents)
    for i in range(len(lines)):
        line = lines[i]
        inst_line = ""
        for y in range(len(line)):
            token = line[y]
            if token[0] == 'symbol':
                if token[1] in Symbols:
                    if token[1] == 'var':
                        inst_line += 'Vars["'
                        if re.match(r'[.a-zA-Z0-9_]+', line[y+1][1]):
                            inst_line += line[y+1][1] + '"] = '
                        else:
                            # throw error
                            break
                        inst_line += line[y+2][1]
                        exec(inst_line)
        
    return lines
