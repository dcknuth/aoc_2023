'''AoC Day1'''

#filename = "test01.txt"
#filename = "test02.txt"
filename = "input01.txt"

with open(filename) as f:
    ls = f.read().strip().split('\n')

total = 0
for l in ls:
    val = []
    for c in l:
        if c.isdigit():
            val.append(c)
            break
    for c in l[::-1]:
        if c.isdigit():
            val.append(c)
            break
    total += int(''.join(val))

print("Part 1 total of values is", total)

nums = {"one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6",
        "seven":"7", "eight":"8", "nine":"9"}

DEBUG = 0
total = 0
for l in ls:
    first_word_position = -1
    first_digit_position = -1
    first_word = ''
    first_digit = ''
    first_num = ''
    # Find the first word-based number
    for n in nums.keys():
        if (cur_pos := l.find(n)) != -1:
            if first_word_position < 0 or first_word_position > cur_pos:
                first_word_position = cur_pos
                first_word = n
    # Find the first digit based number
    for i, c in enumerate(l):
        if c.isdigit():
            first_digit_position = i
            first_digit = c
            break
    # Determine which of the two is first
    if first_word_position == -1 and first_digit_position > -1:
        first_num = first_digit
    elif first_digit_position == -1 and first_word_position > -1:
        first_num = nums[first_word]
    elif first_digit_position > -1 and first_word_position > -1:
        if first_digit_position < first_word_position:
            first_num = first_digit
        else:
            first_num = nums[first_word]
    else:
        print("Error: no first number found in line:")
        print(l)
    if DEBUG > 4:
        print(f"Row: {l} has a first num of {first_num}")
    # Now work on the second digit in a similar way
    second_word_position = -1
    second_digit_position = -1
    second_word = ''
    second_digit = ''
    second_num = ''
    # Find the second word-based number
    for n in nums.keys():
        if (cur_pos := l.rfind(n)) != -1:
            if second_word_position < cur_pos:
                second_word_position = cur_pos
                second_word = n
    # Find the second digit based number
    for i in range(len(l)-1, -1, -1):
        if l[i].isdigit():
            second_digit_position = i
            second_digit = l[i]
            break
    # Determine which of the two is last
    if second_word_position == -1 and second_digit_position > -1:
        second_num = second_digit
    elif second_digit_position == -1 and second_word_position > -1:
        second_num = nums[second_word]
    elif second_digit_position > -1 and second_word_position > -1:
        if second_digit_position > second_word_position:
            second_num = second_digit
        else:
            second_num = nums[second_word]
    else:
        print("Error: no second number found in line:")
        print(l)
    if DEBUG > 4:
        print(f"Row: {l} has a second num of {second_num}")
    # We should have both digits, so add to the total
    if DEBUG > 3:
        print(l)
        print(f"{first_num}    {second_num}")
    total += int(''.join([first_num, second_num]))

print("Sum for part 2 is", total)
