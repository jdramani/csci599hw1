"""
This Script builds cross correlation matrix from given files.
"""

import os
import math


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


def bfcc(data_path, type):
    # ccm_overall -> Cross Correlation Matrix overall
    ccm_overall = [[1 for j in range(0, 256)] for i in range(0, 256)]
    first_flag = 1

    type_path = os.path.join(data_path, type)
    files = os.listdir(type_path)

    if len(files) < 100:
        return

    if type in ["application-octet-stream", "application-xhtml+xml","text-html", "application-pdf", "application-rdf+xml", "application-rss+xml", "application-x-sh", "application-x-tika-msoffice"]:
        return
        end_idx = int(math.ceil(len(files) * 0.25))
    else:
        end_idx = int(math.ceil(len(files) * 0.75))

    files = files[0:end_idx]

    for file in files:

        path = os.path.join(type_path, file)
        # open that file in binary mode and process it
        f = open(path, "rb")

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

        # Now loop over to this list and augment this file to overall matrix
        ccm = [[1 for j in range(0, 256)] for i in range(0, 256)]

        if first_flag == 1:
            # 1) Fill the bottom of diagonal
            for i in range(0, 256):
                for j in range(0, i + 1):
                    ccm[i][j] = bfd[i] - bfd[j]

            # 2) set top-left element to 1 (As this is the first file)
            ccm[0][0] = 1

            ccm_overall = ccm[:][:]
            first_flag = 0
            continue
        else:
            # 1) Fill the bottom of diagonal
            for i in range(0, 256):
                for j in range(0, i + 1):
                    ccm[i][j] = bfd[i] - bfd[j]

            # 2) Fill the upper side of diagonal
            for i in range(0, 255):
                for j in range(i + 1, 256):
                    ccm[i][j] = correlation_factor(abs(ccm[j][i] - ccm_overall[j][i]))

            # 3) Now add this ccm to ccm_overall to form new ccm_overall
            prev_files = ccm_overall[0][0]
            for i in range(0, 256):
                for i in range(0, 256):
                    ccm_overall[i][j] = float(float(ccm_overall[i][j]) * float(prev_files) + float(ccm[i][j])) / float(
                        prev_files + 1)

            ccm_overall[0][0] = prev_files + 1

    # write ccm_overall to csv file...

    out_file = open("../bfcc/" + type + '-cross_corr.csv', 'w')

    out_file.write(",".join(range(0, 256)))
    out_file.write('\n'.join([','.join(ccm_overall[i]) for i in range(0, 256)]))

    out_file.close()


if __name__ == "__main__":
    data_path = "/Users/minhpham/projects/Ass1-ContentDetection/data/"
    for type in os.listdir(data_path):
        if type == ".DS_Store":
            continue
        bfcc(data_path, type)
