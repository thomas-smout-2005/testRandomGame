list = [1, 1, 1, 1, 1]
roll = [1, 2, 3, 4, 5]

keep = input("Keep:")
final = keep.split()

print(final)

list = [0, 0, 0, 0, 0]
for y in range(len(final)):
    position = int(final[y]) - 1
    list[position] = roll[position]

print(list)