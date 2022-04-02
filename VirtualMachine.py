SZAM        = "00000000"
MUVELET     = "00000001"
VALTOZO     = "00000010"
ERTEKADAS   = "00000011"

ADD         = "00000000"
SUB         = "00000001"
MUL         = "00000010"
DIV         = "00000011"

class VirtualMachine:
    
    
    def __init__(self) -> None:
        self.registers = [0]*100
        self.stack = []

    def byteStringToNumber(self, byteString):
        res = 0
        # reversed string
        for i, b in enumerate(byteString[::-1]):
            res += int(b)*2**i
        return res


    def run(self, line, debug):
        # split the bitstring by bytes
        chunk_size = 8
        bytes = [line[i:i+chunk_size] for i in range(0, len(line), chunk_size)]

        # check if it is an assignment
        start = 0 
        lhs_idx = -1
        if(bytes[2] == ERTEKADAS):
            lhs_idx = self.byteStringToNumber(bytes[1])
            lhs = self.registers[lhs_idx]
            start = 3

        # iterate over the byte string
        op = ""
        for i, b in enumerate(bytes[start:]):
            # even indices are the "type markers"
            if(i % 2 == 0):
                if(b == SZAM):
                    op = SZAM

                elif(b == MUVELET):
                    op = MUVELET

                elif(b == VALTOZO):
                    op = VALTOZO

            # odd indices are the actual values - numbers or operations
            # register + number means the numberth register
            else:
                if(op == SZAM):
                    bs = self.byteStringToNumber(b)
                    self.stack.append(bs)
                    print(f"append {bs}")  if debug else 0
                elif(op == MUVELET):
                    if(b == ADD):
                        n = self.stack.pop()
                        m = self.stack.pop()
                        self.stack.append(n+m)
                        print(f"append {n}+{m}") if debug else 0
                    elif(b == SUB):
                        n = self.stack.pop()
                        m = self.stack.pop()
                        self.stack.append(m-n)
                        print(f"append {m}-{n}") if debug else 0
                    elif(b == MUL):
                        n = self.stack.pop()
                        m = self.stack.pop()
                        self.stack.append(n*m)
                        print(f"append {n}*{m}") if debug else 0
                    elif(b == DIV):
                        n = self.stack.pop()
                        m = self.stack.pop()
                        self.stack.append(m/n)
                        print(f"append {m}+{n}") if debug else 0
                elif(op == VALTOZO):
                    register_idx = self.byteStringToNumber(b)
                    print(f"append {self.registers[register_idx]}") if debug else 0
                    self.stack.append(self.registers[register_idx])

        res = self.stack.pop()
        if(lhs_idx != -1):
            self.registers[lhs_idx] = res
        return res


