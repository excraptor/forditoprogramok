from VirtualMachine import VirtualMachine

def main():
    vm = VirtualMachine()
    test = "00000000000010010000000000000001000000000000000100000001000000000000000100000010"
    print(vm.run(test))

if(__name__ == "__main__"):
    main()

