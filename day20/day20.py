'''AoC Day 20 Part 1 - what is the total number of low pulses, multiplied
by the total number of high pulses'''
from collections import defaultdict

filename = "input20.txt"
#filename = "test20-1.txt"
#filename = "test20-2.txt"
RX_SET = False

with open(filename) as f:
    ls = f.read().strip().split('\n')

class ComMod:
    mod_types = {'%':0, '&':1, 'broadcaster':2, 'button':3}
    conjunctions = dict()
    high_sent = 0
    low_sent = 0
    def __init__(self, mtype, name, send_to) -> None:
        self.mtype = mtype
        self.name = name
        self.send_to = send_to
        self.sent_low = 0
        self.sent_high = 0
        if self.mtype == '%':
            self.on_off = 'off'
        if self.mtype == '&':
            self.in_mem = defaultdict(lambda: "low")
            ComMod.conjunctions[self.name] = True
    
    def process(self, signal):
        # depending on type, decide what to send and put into a list with
        #  the format (from_name, to_name, signal_type)
        from_m, to_m, sig_type = signal
        if self.mtype == '%':
            if sig_type == 'low':
                if self.on_off == 'off':
                    self.on_off = 'on'
                    sig_list = []
                    for m in self.send_to:
                        sig_list.append((self.name, m, 'high'))
                        ComMod.high_sent += 1
                        self.sent_high += 1
                    return(sig_list)
                else:
                    self.on_off = 'off'
                    sig_list = []
                    for m in self.send_to:
                        sig_list.append((self.name, m, 'low'))
                        ComMod.low_sent += 1
                        self.sent_low += 1
                    return(sig_list)
            else:
                return([])
        if self.mtype == '&':
            self.in_mem[from_m] = sig_type
            if 'low' not in self.in_mem.values():
                sig_list = []
                for m in self.send_to:
                    sig_list.append((self.name, m, 'low'))
                    ComMod.low_sent += 1
                    self.sent_low += 1
                return(sig_list)
            else:
                sig_list = []
                for m in self.send_to:
                    sig_list.append((self.name, m, 'high'))
                    ComMod.high_sent += 1
                    self.sent_high += 1
                return(sig_list)
        if self.mtype == 'button':
            ComMod.low_sent += 1
            self.sent_low += 1
            return([(self.name, 'broadcaster', 'low')])
        if self.mtype == 'broadcaster':
            sig_list = []
            for m in self.send_to:
                sig_list.append((self.name, m, sig_type))
                if sig_type == 'high':
                    ComMod.high_sent += 1
                    self.sent_high += 1
                else:
                    ComMod.low_sent += 1
                    self.sent_low += 1
            return(sig_list)
        else:
            if self.name == 'rx' and sig_type == 'low':
                RX_SET = True
            return([])

modules = dict()
for l in ls:
    mod, send_to = l.split(' -> ')
    send_to = send_to.split(', ')
    if mod == "broadcaster":
        name = "broadcaster"
        cur_mod = ComMod(mod, name, send_to)
        modules[name] = cur_mod
    elif mod[0] == '%':
        name = mod[1:]
        cur_mod = ComMod(mod[0], name, send_to)
        modules[name] = cur_mod
    elif mod[0] == '&':
        name = mod[1:]
        cur_mod = ComMod(mod[0], name, send_to)
        modules[name] = cur_mod
# fill out the input list memory for the conjunction modules and
#  handle missing output modules
add_list = []
for cur_mod in modules.keys():
    for m in modules[cur_mod].send_to:
        if m in ComMod.conjunctions:
            modules[m].in_mem[cur_mod] = 'low'
        if m not in modules:
            add_list.append(ComMod(m, m, m))
for m in add_list:
    modules[m.name] = m
# add the button
modules['button'] = ComMod('button', 'button', 'broadcaster')

times = 1000
for t in range(times):
    pulses = [('elf', 'button', 'low')]
    while len(pulses) > 0:
        from_m, cur_mod, sig_type = pulses.pop()
        new_pulses = modules[cur_mod].process((from_m, cur_mod, sig_type))
        if len(new_pulses) > 0:
            new_pulses.extend(pulses)
            pulses = new_pulses

print(f"High sent was {ComMod.high_sent} and low sent was {ComMod.low_sent}")
print("After multiplying", ComMod.high_sent * ComMod.low_sent)


'''Part2 - What is the fewest button presses to get a low pulse to rx?
Will try just letting it run first, but sometimes these types require
one to reverse engineer what the system is doing and calculate.
This turns out to be the latter type as it has not resolved after
10,000,000 presses. We will need to print the system state and keep
looking to try to figure out what it is doing and then compute the
needed value.
Let's try looking at a low output cycle for each of the items feeding rx,
there are four, and then finding the LCM of those, as that is a common AoC
way to make the result hard to brute-force'''
# first reset
ComMod.high_sent = 0
ComMod.low_sent = 0
for cur_mod in modules.keys():
    for m in modules[cur_mod].send_to:
        if m in ComMod.conjunctions:
            modules[m].in_mem[cur_mod] = 'low'

times = 1000000000
old_vals = {'tr':0, 'xm':0, 'dr':0, 'nh':0}
presses = {'tr':0, 'xm':0, 'dr':0, 'nh':0}
for t in range(times):
    pulses = [('elf', 'button', 'low')]
    while len(pulses) > 0:
        from_m, cur_mod, sig_type = pulses.pop()
        new_pulses = modules[cur_mod].process((from_m, cur_mod, sig_type))
        if len(new_pulses) > 0:
            new_pulses.extend(pulses)
            pulses = new_pulses
    if RX_SET:
        print("Number of button presses was", t)
        break
    for key in old_vals.keys():
        if modules[key].sent_high != old_vals[key]:
            print(f"{key} changed at button press {t+1}")
            old_vals[key] = modules[key].sent_high
            presses[key] = t + 1
    if all(presses.values()):
        break
    if t % 100000 == 0:
        print(f"We have run {t+1} button presses")

# First changes in each are on presses 2739, 2761, 2797 and 2889
all_pressed = 1
for n in presses.values():
    all_pressed *= n
print("First button press of all at the same time is", all_pressed)

# Needed the second set and to see the difference to the first
#  then the LCM
import math
print("Final answer", math.lcm(3739, 3761, 3797, 3889))