import json
import math
import os
from collections import defaultdict

from submission.utils import compand_fn, add_two_lists, correlation_factor, type_list


def bfdc(input_dir_path, bfa_file, output_file, ratio):
    final_cf = [0] * 256
    count = 0

    files = os.listdir(input_dir_path)

    end_idx = int(math.ceil(len(files) * ratio))

    b_file = open(bfa_file, 'r')
    new_dict = json.load(b_file)
    b_file.close()

    fp = []

    for i in range(0, 256):
        fp.append(float(new_dict[str(i)]))

    files = files[end_idx + 1:]

    for file in files:
        if type[0] == ".":
            continue
        path = os.path.join(input_dir_path, file)

        # open that file in binary mode and process it
        f = open(path, "rb")
        count += 1
        # Initialize array for this file for byte frequency distribution
        bfd = [0 for i in range(0, 256)]

        # Read bytes one by one until the end of file
        while 1:
            byte = f.read(1)

            if not byte:
                break

            bfd[ord(byte)] += 1
        f.close()
        # Normalize the bfd array

        max1 = max(bfd)
        bfd = [float(i) / float(max1) for i in bfd]

        # Companding
        bfd = compand_fn(bfd)

        # Compute correlation factor for this file
        cf = [correlation_factor(abs(bfd[i] - fp[i])) for i in range(0, 256)]
        final_cf = add_two_lists(final_cf, cf)

    final_cf = [float(item) / float(count) for item in final_cf]

    d = defaultdict(float)

    for i in range(0, 256):
        d[str(i)] = final_cf[i]

    out_file = open(output_file, "w")
    json.dump(d, out_file, indent=4)
    out_file.close()


if __name__ == "__main__":
    data_path = "/Users/minhpham/projects/data1"
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
        output_file = '../bfcc/' + type + "-bfcc.json"
        bfdc(type_path, bfa_file, output_file, ratio)
