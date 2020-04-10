from sys import argv


def parse_file(some_file):
    with open(some_file, "r") as f:
        yield from f


if __name__ == "__main__":
    property_set = set([i for i in range(22)])

    contents = parse_file(argv[1])
    with open(argv[2], "w") as fout:
        for line in contents:
            if "=" in line:
                """ Faster to check line[1] == "=", but some lines only have one char, therefore OOB error"""
                # The line is a header.
                fout.write(line[1:])
            else:
                # Unsure of time complexity of the following:
                owned_properties = set([int(i) for i in line.strip().split(',')])
                unowned_properties = property_set.difference(owned_properties)
                fout.write(f'{unowned_properties}'+"\n")