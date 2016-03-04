import math

type_list = ["text-plain", "video-mp4", "application-x-sh", "application-rdf+xml", "application-vnd.ms-excel" ,
             "application-x-tika-ooxml", "application-octet-stream", "video-quicktime", "video-mpeg", "application-x-elc",
             "audio-mp4", "image-tiff", "video-x-ms-wmv", "application-xml", "message-rfc822"]

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