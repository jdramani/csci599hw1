import os

from lxml import etree


def mimetype_generating():
    data_path = "../fht16/"
    for file in os.listdir(data_path):
        if "head" in file:
            values = [[0 for i in range(256)] for j in range(16)]
            path = os.path.join(data_path, file)
            with open(path, 'r') as f:
                for idx, line in enumerate(f.readlines()):
                    if idx == 0:
                        continue
                    values[idx - 1] = [float(i) for i in line.split(',')]
            header_str = ""
            for row_num in range(16):
                found = False
                for pos in range(256):
                    if values[row_num][pos] >= 0.8:
                        header_str += chr(pos)
                        found = True
                if not found:
                    break
            try:
                root = etree.Element("magic")
                root.set('priority', str(int(values[row_num][pos] * 100)))
                match = etree.SubElement(root, "match")
                match.set('value', header_str)
                print header_str
                match.set('type', 'byte')
                match.set('offset', str(row_num))
                with open('magic.xml', 'a') as wf:
                    wf.write(file.rsplit("-", 1)[0] + "\n")
                    wf.write(etree.tostring(root) + "\n")
            except:
                pass

if __name__ == "__main__":
    mimetype_generating()