#!/usr/bin/env python3

import sys

# Solution to the day 19 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/19

# A model of the device.
class Device:
    # OPCODES maps each opcode to a function that implements it.  All
    # functions take four arguments:  a list containing the starting
    # state of the six registers, two inputs (A and B), and an output
    # (C).  All functions return a list containing the resulting register
    # states.
    OPCODES = {'addr': (lambda device, r, a, b, c: device.addr(r,a,b,c)),
               'addi': (lambda device, r, a, b, c: device.addi(r,a,b,c)),
               'mulr': (lambda device, r, a, b, c: device.mulr(r,a,b,c)),
               'muli': (lambda device, r, a, b, c: device.muli(r,a,b,c)),
               'banr': (lambda device, r, a, b, c: device.banr(r,a,b,c)),
               'bani': (lambda device, r, a, b, c: device.bani(r,a,b,c)),
               'borr': (lambda device, r, a, b, c: device.borr(r,a,b,c)),
               'bori': (lambda device, r, a, b, c: device.bori(r,a,b,c)),
               'setr': (lambda device, r, a, b, c: device.setr(r,a,b,c)),
               'seti': (lambda device, r, a, b, c: device.seti(r,a,b,c)),
               'gtir': (lambda device, r, a, b, c: device.gtir(r,a,b,c)),
               'gtri': (lambda device, r, a, b, c: device.gtri(r,a,b,c)),
               'gtrr': (lambda device, r, a, b, c: device.gtrr(r,a,b,c)),
               'eqir': (lambda device, r, a, b, c: device.eqir(r,a,b,c)),
               'eqri': (lambda device, r, a, b, c: device.eqri(r,a,b,c)),
               'eqrr': (lambda device, r, a, b, c: device.eqrr(r,a,b,c))}

    def __init__(self,ip_register,program):
        self.ip_register_ = ip_register
        self.program_ = program
        self.ip_ = 0

    # op code implementations (curse Python's limited lambdas)
    def addr(self,r,a,b,c):
        r[c] = r[a] + r[b]
        return r

    def addi(self,r,a,b,c):
        r[c] = r[a] + b
        return r

    def mulr(self,r,a,b,c):
        r[c] = r[a] * r[b]
        return r

    def muli(self,r,a,b,c):
        r[c] = r[a] * b
        return r

    def banr(self,r,a,b,c):
        r[c] = r[a] & r[b]
        return r

    def bani(self,r,a,b,c):
        r[c] = r[a] & b
        return r

    def borr(self,r,a,b,c):
        r[c] = r[a] | r[b]
        return r

    def bori(self,r,a,b,c):
        r[c] = r[a] | b
        return r

    def setr(self,r,a,b,c):
        r[c] = r[a]
        return r

    def seti(self,r,a,b,c):
        r[c] = a
        return r

    def gtir(self,r,a,b,c):
        if a > r[b]:
            r[c] = 1
        else:
            r[c] = 0
        return r

    def gtri(self,r,a,b,c):
        if r[a] > b:
            r[c] = 1
        else:
            r[c] = 0
        return r

    def gtrr(self,r,a,b,c):
        if r[a] > r[b]:
            r[c] = 1
        else:
            r[c] = 0
        return r

    def eqir(self,r,a,b,c):
        if a == r[b]:
            r[c] = 1
        else:
            r[c] = 0
        return r

    def eqri(self,r,a,b,c):
        if r[a] == b:
            r[c] = 1
        else:
            r[c] = 0
        return r

    def eqrr(self,r,a,b,c):
        if r[a] == r[b]:
            r[c] = 1
        else:
            r[c] = 0
        return r

    # Execute the op code.
    def execute(self,opcode,r,a,b,c):
        return self.OPCODES[opcode](self,r.copy(),a,b,c)


    def run(self):
        r = [1, 0, 0, 0, 0, 0]
        count = 0
        # while (r[self.ip_register_] < len(self.program_)
        #        and (count < 1000 or r[self.ip_register_] <= 11)):
        # while (r[self.ip_register_] < len(self.program_)
        #        and r[3] <= 10551388):
        while r[self.ip_register_] < len(self.program_):
            opcode, a, b, c = program[r[self.ip_register_]]
            print(str(r) + " " + opcode + " ",end='')
            r = self.execute(opcode,r,a,b,c)
            r[self.ip_register_] += 1
            print(str(r) + "  (" + str(count) + ")")
            count += 1
        r[self.ip_register_] -= 1

        return r
    
    # End of Device class.

    
def parse_program(filename):
    """
    Load the program from FILENAME into a list of lists.  Capture the IP
    register and return both.
    """
    ip_register = None
    program = list()

    with open(filename) as f:
        for line in f:
            if line.startswith('#ip '):
                ip_register = int(line.rstrip()[len('#ip '):])
            else:
                opcode, a, b, c = line.rstrip().split(' ')
                program.append([opcode, int(a), int(b), int(c)])

    return [ip_register, program]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ip_register, program = parse_program(sys.argv[1])
        device = Device(ip_register,program)

        print(ip_register)
        print(program)
        print()
        print(device.run())
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
