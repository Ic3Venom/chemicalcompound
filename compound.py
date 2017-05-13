class Info:
    '''Holds information of Elements and Compounds'''
        
    def __init__(self):
        #names in order of file): symbol, mass, name, number, amount
        
        self.amount = 0
        self.name   = ''    #Only applies to Element class
        self.number = 0     #Only applies to Element class
        self.mass   = 0.0
        self.symbol = ''

class Element:
    '''A class to hold elements'''
        
    def change(self, i, value):
        if i == 0:
            self.stat.symbol = str(value)
        elif i == 1:
            self.stat.mass   = float(value)
        elif i == 2:
            self.stat.name   = str(value)
        elif i == 3: 
            self.stat.number = int(value)
        
    def find(self): #Might revert back to single data return
        '''Finds element in table.bin, returns element mass'''

        with open('table.bin', 'rb') as f:
            for line in f:

                if line.split()[0] == self.stat.symbol: #line.split[0] is symbol location
                    for term in range( len(line.split()) ):
                        self.change(term, line.split()[term])
                    
                    break

            else:
                print 'ERROR: unknown element \'%s\'. Exiting program' % self.stat.symbol
                f.close()
                exit(1)

    def subscript(self):
        for i in range(len(self.stat.symbol)):
            if not self.stat.symbol[i].isalpha():
                temp = int(self.stat.symbol[i:])
                self.stat.symbol = self.stat.symbol[:i]
                return temp
        else:   #if self.stat.symbol has no amount attached, defaults to 1
            return 1

    def __init__(self, symbol, compoundAmount):
        self.stat = Info()

        self.stat.symbol = symbol
        self.stat.amount = int(compoundAmount) * self.subscript()

        self.find()
        self.stat.mass = self.stat.mass * self.stat.amount

class Compound:
    '''A class to hold compounds, which hold class(Element)'''
     
    def bracketAmount(self, brackets, i, j):
        for bracket in brackets[1:]:
            if bracket[0] < j and bracket[1] > i:
                return bracket[2]
        else:
            return 1
            
    def analyze(self):
        '''Determines interior elements and puts them in array(inside)'''

        brackets = [1, [0,0,1]] #Index of first bracket info, first bracket info is dummy for symbols who don't have brackets
        
        #For1: searches symbol for brackets, and if found, will put more information of them
        for i in range(len(self.stat.symbol)):

            if self.stat.symbol[i] == '(':
                i += 1 
                brackets.append([i, 0, 1])

            elif self.stat.symbol[i] == ')':
                
                brackets[brackets[0]][1] = i
                for j in range( i, len(self.stat.symbol)):
                    if self.stat.symbol[j].isalpha():
                        brackets[brackets[0]][2] = int(self.stat.symbol[i+1:j-1])
                        brackets[0] += 1
                        break
                    
                else:
                    brackets[brackets[0]][2] = int(self.stat.symbol[j:])
                    break

        #Checks if first char in self.stat.symbol is capitalized or is '('
        if self.stat.symbol[0].isupper():
            i = j = 0
        elif self.stat.symbol[0] == '(':
            i = j = 0
        else: 
            print 'Impossible character \'%s\'. Exiting program.' % self.stat.symbol[0]
            exit(1)
        brackets[0] = 1
        skip = 1
        
        while i < len(self.stat.symbol) and j <= len(self.stat.symbol):
              
            if self.stat.symbol[i] == '(' and skip == 1:
                j += 1
                
            elif self.stat.symbol[i].isupper() and skip == 1:
                skip = None

            elif self.stat.symbol[i].isupper(): #P4
                
                self.inside.append(
                    Element(
                        self.stat.symbol[j:i],
                        self.stat.amount * brackets[brackets[0]][2] ) )
                j = i

            elif self.stat.symbol[i] in ['(', ')']:  #P1
                self.inside.append(
                    Element(
                        self.stat.symbol[j:i],
                        self.stat.amount * brackets[brackets[0]][2] ) )
                
                j += len(str(self.stat.symbol[j:i]))
                
                if self.stat.symbol[i] == ')':                    
                    i += len(str(self.inside[-1].stat.symbol))
                    brackets[0] += 1
            
            i += 1

        else:
            if self.stat.symbol[j:].isalnum():                
                self.inside.append(
                    Element(
                        self.stat.symbol[j:],
                        self.stat.amount ) )

    def coef(self):
        #if Compound has no coefficient, amount defaults to 1
        if not self.stat.symbol[0].isdigit():
            return 1

        for i in range( len( self.stat.symbol)):
            if not self.stat.symbol[i].isdigit():
                temp = self.stat.symbol[:i]
                self.stat.symbol = self.stat.symbol[i:]
                return temp

    def mass(self):
        for i in self.inside:
            self.stat.mass += i.stat.mass

    def __init__(self, symbol):
        self.stat = Info()
        
        self.inside = []

        self.stat.symbol = symbol
        self.stat.amount = self.coef()

        self.analyze()
        self.mass()
        
if __name__ == '__main__':
    test = Compound( raw_input("Compound: ") )
    print test.stat.symbol, self.stat.mass, self.stat.name, self.stat.number, self.stat.amount

    exit(0)
