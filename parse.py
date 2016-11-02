import csv

def read_for_events(filename):
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        new_rows = []
        for row in reader:
            new_row = row[-11], row[3], row[4], row[5]
            new_rows.append(new_row)
        return new_rows
            
def read_for_animals(filename):
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        new_rows = []
        for row in reader:
            new_row = row[-11]
            new_rows.append(new_row)
        new_rows_set = set(new_rows)
        new_rows_list = list(new_rows_set)
        return new_rows_list

def write_for_events(filename, lines):
    with open(filename, 'wb') as file:
        csv.writer(file, delimiter='|').writerows(lines)

def write_for_animals(filename, lines):
    with open(filename, 'wb') as export:
        for line in lines:
            export.write('{}|h\n'.format(line))


event_rows = read_for_events('humpback-whale-data.csv')
write_for_events('seed_data/u.event', event_rows)

animal_rows = read_for_animals('humpback-whale-data.csv')
write_for_animals('seed_data/u.animal', animal_rows)


        




