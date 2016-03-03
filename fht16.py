import os
import math


def fht(data_path, type):
    #####  4-header  ######
    count_4 = 16
    head_4_overall = [[0 for i in range(0, 256)] for j in range(0, count_4)]
    first_flag = 1
    file_count = 0

    type_path = os.path.join(data_path, type)

    files = os.listdir(type_path)

    if len(files) < 100:
        return

    if type in ["application-octet-stream", "application-xhtml+xml", "text-html"]:
        return
        end_idx = int(math.ceil(len(files) * 0.25))
    else:
        end_idx = int(math.ceil(len(files) * 0.75))

    files = files[:end_idx]

    # Go Through Each File in a particular directory
    for file in files:
        path = os.path.join(type_path, file)

        f = open(path, "rb")
        head4 = [[0 for file in range(0, 256)] for j in range(0, count_4)]
        # Read bytes till count
        for file in range(0, count_4):
            byte = f.read(1)
            if byte:
                byte_index = ord(byte) - 1
                head4[file][byte_index] = 1
            else:
                head4[file] = [-1] * 256

        if first_flag == 1:
            head_4_overall = head4[:][:]
            first_flag = 0
            file_count += 1
            continue
        else:
            for k in range(0, count_4):
                for j in range(0, 256):
                    head_4_overall[k][j] = float(float(head_4_overall[k][j]) * file_count + head4[k][j]) / float(
                        file_count + 1)
            file_count += 1

        f.close()

    # write head4overall to csv file...

    out_file = open('../fht16/' + type + '-head4overall.csv', 'w')

    out_file.write(",".join([str(i) for i in range(0, 256)]) + "\n")
    out_file.write('\n'.join([','.join([str(j) for j in head_4_overall[i]]) for i in range(0, count_4)]))

    out_file.close()

    ########  4-Trailer #############

    count_4 = 16
    trail_4_overall = [[0 for i in range(0, 256)] for j in range(0, count_4)]
    first_flag = 1
    file_count = 0
    # Go Through Each File in a particular directory
    for file in files:
        path = os.path.join(type_path, file)

        f = open(path, "rb")
        f.seek(0, 2)
        size = f.tell()
        m = count_4 - 1

        trail4 = [[0 for file in range(0, 256)] for j in range(0, count_4)]
        while size > 0 and m >= 0:
            size -= 1
            f.seek(size)
            byte = f.read(1)
            if byte:
                byte_index = ord(byte) - 1
                trail4[m][byte_index] = 1
            else:
                trail4[m] = [-1] * 256
            m -= 1

        if first_flag == 1:
            trail_4_overall = trail4[:][:]
            first_flag = 0
            file_count += 1
            continue
        else:
            for k in range(0, count_4):
                for j in range(0, 256):
                    trail_4_overall[k][j] = float(
                        float(trail_4_overall[k][j]) * file_count + trail4[k][j]) / float(
                        file_count + 1)
            file_count += 1

        f.close()

    # write trail4overall to csv file...

    out_file = open('../fht16/' + type + '-trail4overall.csv', 'w')

    out_file.write(",".join([str(i) for i in range(0, 256)]) + "\n")
    out_file.write('\n'.join([','.join([str(j) for j in trail_4_overall[i]]) for i in range(0, count_4)]))

    out_file.close()


if __name__ == "__main__":
    data_path = "/Users/minhpham/projects/Ass1-ContentDetection/data/"
    for type in os.listdir(data_path):
        if type == ".DS_Store":
            continue
        fht(data_path, type)
