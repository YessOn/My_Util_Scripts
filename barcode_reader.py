from random import randint

LEFT = [[39, 51, 27, 33, 29, 57, 5, 17, 9, 23], [13, 25, 19, 61, 35, 49, 47, 59, 55, 11]]
RIGHT = [114, 102, 108, 66, 92, 78, 80, 68, 72, 116]
EO_TABLE = [63, 52, 50, 49, 44, 38, 35, 42, 41, 37]
start, center, end = '101', '01010', '101'

# Define Util Functions
bin2dec = lambda i: int(str(i), 2)

# Standard Solver
def solver(barcode):
    if barcode[0:3] == start and barcode[45:50] == center and barcode[92:95] == end and '0000000' not in barcode:
        # Slice Right hand and Left hand Values
        the_left = barcode[3:45]
        the_right = barcode[50:92]

        answer = []

        # Combining Bits of first digit to convert to decimal
        fd_binary = ''

        # Format Left Characters
        my_digits = [the_left[7*i:7*(i+1)] for i in range(0, 6)]
        for i in my_digits:
            for j in LEFT:
                try:
                    digit = j.index(bin2dec(i))
                    # a is the Partial collection of the first digit
                    if digit >= 0:
                        a = LEFT.index(j)
                except:
                    pass
            fd_binary += str(a)
            answer.append(digit)
        answer.insert(0, EO_TABLE.index(bin2dec(fd_binary)))

        # Format Right Characters
        my_digits = [the_right[7*i:7*(i+1)] for i in range(0, 6)]
        for i in my_digits:
            answer.append(RIGHT.index(bin2dec(i)))

        # Looking for the Checksum [Check digit]
        cd = 10 - sum(a*(1, 3)[i % 2] for i, a in enumerate(answer[:-1])) % 10
        cd = cd if cd < 10 else 0
        if cd != answer[-1]:
            return None

        # Return the joined answer
        return ''.join(map(str, answer))
def barcode_reader(barcode):
    # Translate BarCode To Binary
    barcode = barcode.translate(str.maketrans(' _', '01'))
    try: # While not Backward
        return solver(barcode)
    except: # Where Backward
        barcode = barcode[::-1]
        return solver(barcode)

# Some Examples

print(barcode_reader('_ _   _ __ _  ___ __  __  _  __ ____ _  ___ _ _ _ __  __ __ __  _    _ _ ___  _  ___ _   _  _ _'))
# >> 5901234123457
print(barcode_reader('_ _   __ _ _  ___ ____ _   _ __  _ ___  ___ _ _ _ __  __ _  ___ _  ___ _ ___  _  _   _ _    _ _'))
# >> 4003994155486
print(barcode_reader('_ _ __   _ ___  _ ___ __ _  ___   _  _   _ __ _ _ __ __  _  _   _  _   __  __ _ _    __  __ _ _'))
# >> 8557089288161
print(barcode_reader('_ _ ___ __  __  _  _  __ ____ _ _   __ __   _ _ _ _ _    _   _  _  _   ___ _  __  __ __  __ _ _'))
# >> 0712345678911
print(barcode_reader('_ _ __  __ __  __  _ ___   _  _  _   _    _ _ _ _ _   __ __   _ _ ____ __  _  _  __  __ ___ _ _'))
# >> 0712345678911
print(barcode_reader('_ _   _ __  __  _ _  ___  ___ _  _ ___ ___ __ _ _ _ _    _  ___ _    _ _ _    __  __ ___  _ _ _'))
# >> 3910497653610
print(barcode_reader('_ _ ___ __  __  _        ____ _ _   __ __   _ _ _ _ _    _   _  _  _   ___ _  __  __ __  __ _ _'))
# >> None
print(barcode_reader('_ _ ___ __  __  _  _  __ ____ _ _   __ __   _ _ _ _ _    _   _  _  _   ___ _  __  __ __ __  _ _'))
# >> None
print(barcode_reader('___  _  __  _ ___   _ __ _ ____   _  _  _   _ _ _ _ _    __  __ _    _ _ _    _ _    _  ___ _ _'))
# >> None
print(barcode_reader('_ _  _  __  _ ___   _ __ _ ____   _  _  _   _ _ ___ _    __  __ _    _ _ _    _ _    _  ___ _ _'))
# >> None
print(barcode_reader('_ _  _  __  _ ___   _ __ _ ____   _  _  _   _ _ _ _ _    __  __ _    _ _ _    _ _    _  ___ ___'))
# >> None

   ####   ####  #   #  ####
  #   #  #  #  # # #  ####
 #####  ####  #   #  ####
