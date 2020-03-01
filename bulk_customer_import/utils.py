import csv


def parse_csv(filename):
    output = []
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        for row in reader:
            for item in row:
                row[item] = row[item].strip()
            output.append(row)
    return output
