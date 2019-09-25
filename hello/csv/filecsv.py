import csv
import pandas
from pandas import DataFrame


def list_all_data_from_csv():
    with open('data.csv', 'rt')as f:
        data = csv.reader(f)
        for row in data:
            print(row)


def dict_reader():
    reader = csv.DictReader(open('data.csv'))
    for raw in reader:
        print(raw)


def write_csv_file():
    with open('data_written.scv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Programming language', 'Designed by', 'Appeared', 'Extension'])
        writer.writerow(['Python', 'Guido van Rossum', '1991', '.py'])
        writer.writerow(['Java', 'James Gosling', '1995', '.java'])
        writer.writerow(['C++', 'Bjarne Stroustrup', '1985', '.cpp'])


def panda_read_csv():
    result = pandas.read_csv('data.csv')
    print(result)


def panda_write_csv():
    data = {'Programming language': ['Python','Java', 'C++'],
        'Designed by': ['Guido van Rossum', 'James Gosling', 'Bjarne Stroustrup'],
        'Appeared': ['1991', '1995', '1985'],
        'Extension': ['.py', '.java', '.cpp'],
    }

    data_frame = DataFrame(data, columns=['Programming language', 'Designed by', 'Appeared', 'Extension'])
    export_csv = data_frame.to_csv(r'panda_csv.csv', index=None, header=True)
    print(data_frame)


def main():
    panda_write_csv()


# dict_reader()
# list_all_data_from_csv()


main()
