import csv
import uuid

def write_to_csv(dict_data,csv_columns):
    csv_file = f"{str(uuid.uuid4())}.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns,extrasaction="ignore")
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    return csv_file
