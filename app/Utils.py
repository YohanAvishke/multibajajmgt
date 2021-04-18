import csv
import json
from collections import OrderedDict


def csv_to_json(file_path=None, field_names=None, data_obj=None):
    """
    data_obj  should be [OrderedDict(), ...]
    """
    objects = []

    if file_path is not None:
        file = open(file_path, 'r')
        data_obj = csv.DictReader(file, field_names)

    for idx, row in enumerate(data_obj):
        if idx != 0:
            objects.append(row)
    objects = json.dumps(objects, indent=4)
    objects = json.loads(objects)

    return objects


def find_duplicates(first_file, first_header, second_file, second_header):
    """
    Detect duplicates in the final csv files
    """
    first_reader = open(first_file, 'r')
    second_reader = open(second_file, 'r')

    first_list = list(csv.DictReader(first_reader, first_header))
    second_list = list(csv.DictReader(second_reader, second_header))

    for product_row_one in first_list:
        flag = False
        for product_row_two in second_list:
            if product_row_one['Internal Reference'] == product_row_two['Internal Reference']:
                if flag:
                    print(f'Duplicate {product_row_one["Internal Reference"]}')
                flag = True
