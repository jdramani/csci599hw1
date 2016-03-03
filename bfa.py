import os
import json
from collections import defaultdict

import math


def add_two_lists(l1, l2):
    result = []
    n = len(l1)
    for i in range(0, n):
        result.append(l1[i] + l2[i])

    return result


def compand_fn(l1):
    b = 1.5
    result = []
    n = len(l1)
    for i in range(0, n):
        result.append(pow(float(l1[i]), float(float(1) / float(b))))
    return result


def bfa(data_path, type):
    overall_bfd = [0 for i in range(0, 256)]
    count = 0

    type_path = os.path.join(data_path, type)
    files = os.listdir(type_path)

    if len(files) < 100:
        return

    if type == "application-octet-stream":
        return
        end_idx = int(math.ceil(len(files) * 0.25))
    else:
        end_idx = int(math.ceil(len(files) * 0.75))

    files = files[0:end_idx]

    for file in files:
        if file == ".DS_Store":
            continue
        # open that file in binary mode and process it
        f = open(os.path.join(type_path, file), "rb")
        count += 1
        # Initialize array for this file for byte frequency distribution
        bfd = [0 for i in range(0, 256)]

        # Read bytes one by one until the end of file
        while 1:
            byte = f.read(1)

            if not byte:
                break

            bfd[ord(byte) - 1] += 1
        f.close()
        # Normalize the bfd array

        max1 = max(bfd)
        bfd = [float(file) / float(max1) for i in bfd]

        # Companding
        bfd = compand_fn(bfd)

        overall_bfd = add_two_lists(overall_bfd, bfd)

    overall_bfd = [float(overall_bfd[i]) / float(count) for i in range(0, 256)]

    d = defaultdict()

    for i in range(0, 256):
        d[str(i)] = str(overall_bfd[i])

    out_file = open("../bfa/" + type + "-bfa.json", "w")
    json.dump(d, out_file, indent=4)
    out_file.close()


if __name__ == "__main__":
    data_path = "/Users/minhpham/projects/Ass1-ContentDetection/data/"
    for type in os.listdir(data_path):
        if type == ".DS_Store":
            continue
        bfa(data_path, type)
