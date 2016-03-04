import os
import math

from submission.utils import type_list


def fht(input_dir_path, output_file, h_size, ratio):
    head_4_overall = [[0 for i in range(0, 256)] for j in range(0, h_size)]
    first_flag = 1
    file_count = 0

    files = os.listdir(input_dir_path)

    end_idx = int(math.ceil(len(files) * ratio))

    files = files[0:end_idx]

    # Go Through Each File in a particular directory
    for file in files:
        if file[0] == ".":
            continue

        path = os.path.join(input_dir_path, file)

        f = open(path, "rb")
        head4 = [[0 for i in range(0, 256)] for j in range(0, h_size)]
        # Read bytes till count
        for i in range(0, h_size):
            byte = f.read(1)
            if byte:
                byte_index = ord(byte)
                head4[i][byte_index] = 1
            else:
                head4[i] = [-1] * 256

        if first_flag == 1:
            head_4_overall = head4[:][:]
            first_flag = 0
            file_count += 1
            continue
        else:
            for k in range(0, h_size):
                for j in range(0, 256):
                    head_4_overall[k][j] = float(float(head_4_overall[k][j]) * file_count + head4[k][j]) / float(
                        file_count + 1)
            file_count += 1

        f.close()

    # write head4overall to csv file...

    out_file = open(output_file + '-head4overall.csv', 'w')

    out_file.write(",".join([str(i) for i in range(0, 256)]) + "\n")
    out_file.write('\n'.join([','.join([str(j) for j in head_4_overall[i]]) for i in range(0, h_size)]))

    out_file.close()

    trail_4_overall = [[0 for i in range(0, 256)] for j in range(0, h_size)]
    first_flag = 1
    file_count = 0
    # Go Through Each File in a particular directory

    for file in files:
        if file[0] == ".":
            continue
        path = os.path.join(input_dir_path, file)

        f = open(path, "rb")
        f.seek(0, 2)
        size = f.tell()
        m = h_size - 1

        trail4 = [[0 for i in range(0, 256)] for j in range(0, h_size)]
        while size > 0 and m >= 0:
            size -= 1
            f.seek(size)
            byte = f.read(1)
            if byte:
                byte_index = ord(byte)
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
            for k in range(0, h_size):
                for j in range(0, 256):
                    trail_4_overall[k][j] = float(
                        float(trail_4_overall[k][j]) * file_count + trail4[k][j]) / float(
                        file_count + 1)
            file_count += 1

        f.close()

    # write trail4overall to csv file...

    out_file = open(output_file + '-trail4overall.csv', 'w')

    out_file.write(",".join([str(i) for i in range(0, 256)]) + "\n")
    out_file.write('\n'.join([','.join([str(j) for j in trail_4_overall[i]]) for i in range(0, h_size)]))

    out_file.close()


if __name__ == "__main__":
    data_path = "/Users/minhpham/projects/data1/"
    for type in os.listdir(data_path):
        if type[0] == ".":
            continue
        if type not in type_list:
            continue
        type_path = os.path.join(data_path, type)
        if type == "application-octet-stream":
            ratio = 0.25
        else:
            ratio = 0.75
        bfa_file = '../bfa/' + type + "-bfa.json"
        output_file = '../fht/' + type
        fht(type_path, output_file, 16, ratio)
