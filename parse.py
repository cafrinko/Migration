import csv

def read_raw_data(filename):
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        new_rows = []
        for row in reader:
            new_row = row[-11], row[3], row[4], row[5]
            new_rows.append(new_row)
        return new_rows
            
def write_seed_data(filename, lines):
    with open(filename, 'wb') as file:
        csv.writer(file, delimiter='|').writerows(lines)

rows = read_raw_data('humpback-whale-data.csv')
write_seed_data('seed_data/u.event', rows)

        




