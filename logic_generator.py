from parsers.log_lexer import lexer_wff_data
from parsers.parser_pl_syntax import pl_syntax_parser
from parsers.parser_val import truth_value_parser
from itertools import product, chain
from tabulate import tabulate

class Symbols:
    def __init__(self, s):
        self.s = s
        self.lexer_list = lexer_wff_data(s)

class WffValidator(Symbols):
    def __init__(self, s):
        super().__init__(s) 

    def valid_wff(self):
        self.parser = pl_syntax_parser # yacc.yacc()
        result = self.parser.parse(self.s) # calls parse on the string
        return result
    
    def print_valid_wff(self):
        result = self.valid_wff()        
        if result != None: 
            print(f"{result} is a well-formed formula.")

# TODO: ADD Class is satisfiable, tautology, etc.

class TruthTable(Symbols):
    def __init__(self, s):
        super().__init__(s)
        self.lexer_list = lexer_wff_data(s)
        validator = WffValidator(s)
        self.wff = validator.valid_wff()
        self.s_formula = self.p_letters()
        self.lit_n_dist = self.n_dist_prop_letters()
        self.interpretation = self.interpret_letters()
        self.tv_assignment_dict = self.assign_values_letters_dict()
        self.tv_strings = self.prepare_tv_strings_for_parser()
        self.headers = self.get_headers()

    # LETTERS from the Lexer
    def p_letters(self):
        p_letters = [i[1] for i in self.lexer_list if i[0] == 'LETTER']
        return p_letters
    
    def get_headers(self):        
        headers = []
        for let in self.s_formula:
            if let in headers:
                pass
            else:
                headers.append(let)
        headers.append(self.wff)
        #print(headers)
        return headers

    # Gets num of distinct letters from the s
    def n_dist_prop_letters(self):
        letters = []
        for i in self.lexer_list:
            if i[0] == 'LETTER' and i[1] not in letters:
                letters.append(i[1])
        return len(letters)

    # Gets the matrix of interpretations: 2^n. So 2 letters = 4, 3 letters = 8.
    def interpret_letters(self) -> list:
        return [list(i) for i in product([1, 0], repeat = self.lit_n_dist)]

    # Takes the t-value interpretation and attaches it to the prop letter
    def assign_values_letters_dict(self) -> list:
        letters = [i[1] for i in self.lexer_list if i[0] == 'LETTER']
        assignment = [dict(zip(letters, i)) for i in self.interpretation]
        return assignment

    # Takes list of dicts of letter and t-values (e.g., {'A':1}) and returns a list of strings based on the input string and the interpretation. If User inputs A^B, it will return 1^1, 1^0, 0^1 and 0^0. This is then fed to the valuation_parser to calculate the formula's truth value
    def prepare_tv_strings_for_parser(self):
        t_value_strings = []
        for i in self.tv_assignment_dict:
            temp_list = []
            for tok in self.lexer_list:
                if tok[0] == "LETTER":
                    let = tok[1]
                    val = i[let]
                else:
                    val = tok[1]
                temp_list.append(val)
            wff = "".join(str(item) for item in temp_list)
            t_value_strings.append(wff)
        return t_value_strings

    # Constructs a row of the interpretation of prop letters and the valuation of the main wff. Used for tabulate
    def int_val(self):
        val = [truth_value_parser.parse(i) for i in self.tv_strings]
        for i, j in zip(self.interpretation, val):
            i.append(j)
        #print(self.interpretation)
        return self.interpretation

    # Method for printing the table. By default, fancy outline, centered. To change, we can pass in args. Align args: right, center, left. See tabulate for tablefmt option: https://pypi.org/project/tabulate/
    def print_table(self, tablefmt="plain", numalign="center"):
        int_val = self.int_val()
        #s_formula = self.s_formula
        headers = self.headers
        print(tabulate(int_val, headers=headers, tablefmt=tablefmt, numalign=numalign))
        table = tabulate(int_val, headers=headers, tablefmt=tablefmt, numalign=numalign)
        return table

def main():
    while True:
        try:
            s = input("wff > ")
        except EOFError:
            break
        if not s: continue

        wff = WffValidator(s)
        wff.print_valid_wff()
        table = TruthTable(s)
        table.print_table()

if __name__ == "__main__":
    main()