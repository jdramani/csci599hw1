import os
import math
import json
from collections import defaultdict


###  Load file type's fingerprint ###


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


def correlation_factor(x):
    a = float(pow(x, 2)) * float(-1)
    b = float(2) * float(pow(0.0375, 2))
    y = pow(math.e, float(a / b))
    return y


def avgcalc(l1):
    n = len(l1)
    sum1 = 0
    for item in l1:
        sum1 += item
    return float(sum1) / float(n)


def bfdc(data_path, type):
    final_cf = []
    count = 0
    type_path = os.path.join(data_path, type)
    files = os.listdir(type_path)

    if len(files) < 100:
        return

    if type in ["application-octet-stream", "application-xhtml+xml", "text-html"]:
        return
        end_idx = int(math.ceil(len(files) * 0.25))
    else:
        end_idx = int(math.ceil(len(files) * 0.75))

    in_file = open('../bfa/' + type + "-bfa.json", "r")
    new_dict = json.load(in_file)
    in_file.close()

    fp = []

    for i in range(0, 256):
        fp.append(float(new_dict[str(i)]))

        files = files[0:end_idx]

    for file in files:
        path = os.path.join(type_path, file)

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

            bfd[ord(byte) - 1] += 1
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
        print i
        d[str(i)] = final_cf[i]

    out_file = open('../bfcc/' + type + "-bfcc.json", "w")
    json.dump(d, out_file, indent=4)
    out_file.close()


if __name__ == "__main__":
    data_path = "/Users/minhpham/projects/Ass1-ContentDetection/data/"
    for type in os.listdir(data_path):
        if type == ".DS_Store":
            continue
        bfdc(data_path, type)
