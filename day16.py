#!/usr/bin/env python3

import sys

# Solution to the day 16 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/16

# A model of the device.
class Device:
    # OPCODES maps each opcode to a function that implements it.  All
    # functions take four arguments:  a list containing the starting
    # state of the four registers, two inputs (A and B), and an output
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

    # End of Device class.

    
def parse_samples(filename):
    """ Load the samples from FILENAME into a list of dicts. """
    samples = list()

    with open(filename) as f:
        sample = dict()
        for line in f:
            line = line.rstrip()
            if len(line) > 0:
                if line.startswith("Before: "):
                    sample['Before'] = eval(line[len("Before: "):].strip(),
                                            {'__builtins__':None}, {})
                elif line.startswith("After: "):
                    sample['After'] = eval(line[len("After: "):].strip(),
                                           {'__builtins__':None}, {})
                    samples.append(sample)
                    sample = dict()
                else:
                    sample['Instruction'] = [int(x) for x
                                             in line.strip().split(' ')]

    return samples


if __name__ == "__main__":
    if len(sys.argv) == 2:
        samples = parse_samples(sys.argv[1])
        device = Device()

        three_or_more = 0
        for sample in samples:
            id, a, b, c = sample['Instruction']
            r = sample['Before']
            count = 0
            for opcode in Device.OPCODES:
                if sample['After'] == device.execute(opcode,r,a,b,c):
                    count += 1
            if count >= 3:
                three_or_more += 1
                
        print(three_or_more)
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
