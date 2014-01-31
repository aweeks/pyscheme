import string

s = "(+ 1 (* 2 4))"

s_l = ["(", "+", "1", "(", "*", "2", "4", ")", ")"]

DEBUG = False

class Identifier(object):
    def __init__(self, name):
        self.name = name

class Tokenizer(object):
    
    IDENTIFIER = 1
    BOOLEAN = 2
    NUMBER = 3
    CHARACTER = 4
    STRING = 5
    LPAREN = 6
    RPAREN = 7
    LBANG = 9
    SINGLEQ = 10
    NIL = 11
    COMMA = 12
    PERIOD = 13

    def __init__(self, s):
        self.ptr = 0
        self.s = s
        self.token = ""
        self.tokens = []

        self.tokenized()

        print self.tokens

    def tokenized(self):
        while True:
            self._token()
            if self.token is "":
                return
            else:
                print "found: %s" % (self.token,)
                self.token = ""


    def _peek(self, n=1):
        return self.s[self.ptr : self.ptr+n]

    def _accept(self, *matches):
        print "_accept"

        if len(matches) is 0 and self._peek() != '':
            self.token += self._peek()
            self.ptr += 1
            return True

        for m in matches:
            if self._peek(len(m)) == m:
                self.token += m
                self.ptr += len(m)
                return True
        return False

    def _star(self, fn):
        while True:
            if not fn():
                return True

    def _until(self, *chars):
        return False
    
    def _token(self):
        print "_token"
        
        self._intertoken_space()

        if self._identifier():
            self.tokens.append( (self.IDENTIFIER, self.token) )
        elif self._boolean():
            self.tokens.append( (self.BOOLEAN, True if self.token == '#t' else False) )
        elif self._number():
            self.tokens.append( (self.NUMBER, int(self.token)) )
        elif self._character():
            self.tokens.append( (self.CHARACTER, self.token) )
        elif self._string():
            self.tokens.append( (self.STRING, self.token) )
        elif self._accept('('):
            self.tokens.append( (self.LPAREN, self.token) )
        elif self._accept(')'):
            self.tokens.append( (self.RPAREN, self.token) )
        elif self._accept('#('):
            self.tokens.append( (self.LBANG, self.token) )
        elif self._accept('\''):
            self.tokens.append( (self.SINGQ, self.token) )
        elif self._accept('`{}'):
            self.tokens.append( (self.NILL, self.token) )
        elif self._accept(','):
            self.tokens.append( (self.COMMA, self.token) )
        elif self._accept('.'):
            self.tokens.append( (self.PERIOD, self.token) )
        else:
            return False
        return True
        
    def _delimiter(self):
        print "_delimiter"
        return self._whitespace() or \
               self._any('(', ')', '"', ';')
    
    def _whitespace(self):
        print "_whitespace"
        return self._accept(' ', '\n')
    
    def _comment(self):
        print "_comment"
        return False
        #return self._accept(';') and self._until('\n')
    
    def _atmosphere(self):
        print "_atmosphere"
        return self._whitespace() or self._comment()
    
    def _intertoken_space(self):
        print "_intertoken_space"
        return self._star(self._atmosphere)
    
    def _identifier(self):
        print "_identifier"
        return (self._initial() and \
                self._star(self._subsequent)) or \
                self._peculiar_identifier()
    
    def _initial(self):
        print "_initial"
        return self._letter() or \
               self._special_initial()
    
    def _letter(self):
        print "_letter"
        if self._peek() in string.letters:
            return self._accept()
        else:
            return False
        
    def _special_initial(self):
        print "_special_initial"
        return self._accept('!', '\\$', '\%', '\\verb"&"', '*', '/', ':', '<', '=', '>', '?', '\\verb" "', '\\verb"_"', '\verb"^"')

    def _subsequent(self):
        print "_subsequent"
        return self._initial() or \
               self._digit() or \
               self._special_subsequent()
    
    def _digit(self):
        print "_digit"
        if self._peek() in string.digits:
            return self._accept()
        else:
            return False

    def _special_subsequent(self):
        print "_special_subsequent"
        return self._accept('.', '+', '-')

    def _peculiar_identifier(self):
        print "_peculiar_identifier"
        return self._accept('+', '-', '...')

    def _syntactic_keyword(self):
        print "_syntactic_keyword"
        return self._expression_keyword() or \
               self._accept('else', '=>', 'define', 'unquote', 'unquote-splicing')

    def _expression_keyword(self):
        print "_expression_keyword"
        return self._accept('quote', 'lambda', 'if', 'set!', 'begin', 'cond', 'and', 'or', 'case', 'let', 'let*', 'letrec', 'do', 'delay', 'quasiquote')

    def _boolean(self):
        print "_boolean"
        return self._accept('#t', '#f')

    def _character(self):
        print "_character"
        return False
    
    def _character_name(self):
        print "_character_name"
        return self._accept(' ', '\\n')

    def _string(self):
        print "_string"
        return self._accept('"') and \
               self._star(self._string_element) and \
               self._accept('"')

    def _string_element(self):
        print "_string_element"
        if not self._peek() in ['"', '\\']:
            return self._accept()
        else:
            return False
    
    def _number(self):
        print "_number"
        return self._digit() and self._star(self._digit)
        


