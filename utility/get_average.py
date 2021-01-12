import csv

NUM_OF_FILES = 5

framework = ['flaskAPI', 'fastAPI']
types = ['imageurl', 'base64', 'multipart']

for f_work in framework:
    for methods in types:

        average_request_count = 0
        average_response_time = 0
        average_content_size = 0
        average_request_per_second = 0

        for i in range(1,6):
            filename = '../' + f_work + '/reports/' + methods + '_' + str(i) + '_stats.csv'
            with open(filename, mode='r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader, None)
                for row in reader:
                    average_request_count += float(row[2])
                    average_response_time += float(row[5])
                    average_content_size += float(row[8])
                    average_request_per_second += float(row[9])
                    break

        print(f_work+'_'+methods,
                average_request_count / NUM_OF_FILES,
                average_response_time / NUM_OF_FILES,
                average_content_size / NUM_OF_FILES,
                average_request_per_second / NUM_OF_FILES)

