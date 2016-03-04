import math
import os

from submission.utils import compand_fn, correlation_factor, type_list


def bfcc(input_dir_path, output_file, ratio):
    # ccm_overall -> Cross Correlation Matrix overall
    ccm_overall = [[1 for j in range(0, 256)] for i in range(0, 256)]
    first_flag = 1

    files = os.listdir(input_dir_path)

    end_idx = int(math.ceil(len(files) * ratio))

    files = files[0:end_idx]

    for file in files:

        if file[0] == ".":
            continue

        path = os.path.join(input_dir_path, file)
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

    out_file = open(output_file, 'w')

    out_file.write(",".join([str(i) for i in range(0, 256)]) + "\n")
    out_file.write('\n'.join([','.join([str(j) for j in ccm_overall[i]]) for i in range(0, 256)]))

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
        output_file = "../bfcc/" + type + '-cross_corr.csv'
        bfcc(type_path, output_file, ratio)
