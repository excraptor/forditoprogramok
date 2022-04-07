SZAM        = "00000000"
MUVELET     = "00000001"
VALTOZO     = "00000010"
ERTEKADAS   = "00000011"
READ        = "00000100"

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
        print(bytes) if debug else 0
        # check if it is an assignment
        start = 0 
        lhs_idx = -1
        if(len(bytes) > 2 and bytes[2] == ERTEKADAS):
            print(f"bytes[1]: {bytes[1]}") if debug else 0
            lhs_idx = self.byteStringToNumber(bytes[1])
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
                elif(b == READ):
                    print("read") if debug else 0
                    op = READ

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
                    print(f"register_idx: {register_idx}") if debug else 0
                    print(f"append {self.registers[register_idx]}") if debug else 0
                    self.stack.append(self.registers[register_idx])
                elif(op == READ):
                    register_idx = self.byteStringToNumber(b)
                    print(f"read {register_idx}") if debug else 0
                    try:
                        self.registers[register_idx] = int(input(f"New value for m[{register_idx}]: "))
                        self.stack.append(self.registers[register_idx])
                    except:
                        print("Please enter an integer")
                        exit()

        res = self.stack.pop()
        if(lhs_idx != -1):
            self.registers[lhs_idx] = res
        return res


