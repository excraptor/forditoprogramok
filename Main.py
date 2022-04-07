import enum
from VirtualMachine import VirtualMachine
import sys

def main(args):
    vm = VirtualMachine()
    #test = "00000000000010010000000000000001000000000000000100000001000000000000000100000010"
    # test =   "000000100000000000000011000000000000000100000000000000010000000100000000"
    # tests = ["000000100000000000000011000000000000000100000000000000010000000100000000",
    #          "000000100000000100000011000000000000001000000010000000000000000100000000",
    #          "000000000000001000000010000000010000000100000000"]
    # print(vm.run(tests[0]))
    # print(vm.registers[0])
    debug = False
    if(len(args) > 2 and args[2] == "--debug"):
        debug = True
    with open(args[1]) as f:
        for test in f.readlines():
            print(vm.run(test.strip(), debug))
    for idx, r in enumerate(vm.registers):
        if (r != 0): print(f"register: {idx}\tvalue: {r}")
    
if(__name__ == "__main__"):

    main(sys.argv)

