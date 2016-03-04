import os
import json
from collections import defaultdict

import math

from submission.utils import compand_fn, add_two_lists, type_list


def bfa(input_dir_path, output_file, ratio):
    overall_bfd = [0 for i in range(0, 256)]
    count = 0

    files = os.listdir(input_dir_path)

    end_idx = int(math.ceil(len(files) * ratio))

    files = files[0:end_idx]

    for file in files:
        if file[0] == ".":
            continue
        # open that file in binary mode and process it
        f = open(os.path.join(input_dir_path, file), "rb")
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

        overall_bfd = add_two_lists(overall_bfd, bfd)

    overall_bfd = [float(overall_bfd[i]) / float(count) for i in range(0, 256)]

    d = defaultdict()

    for i in range(0, 256):
        d[str(i)] = str(overall_bfd[i])

    out_file = open(output_file, "w")
    json.dump(d, out_file, indent=4)
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
        output_file = "../bfa/" + type + "-bfa.json"
        bfa(type_path, output_file, ratio)
