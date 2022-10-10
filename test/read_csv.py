import csv
import re

zipname = '/home/bitwalk/ダウンロード/dcp_test_PHC_01_KT_201707012100_202210071845.zip'
csvname = '/home/bitwalk/ダウンロード/dcp_test_PHC_01_KT_201707012100_202210071845.csv'
csvname_2 = '/home/bitwalk/ダウンロード/dcp_test_PHC_01_KT_201707012100_202210071845_wo_oes.csv'

if __name__ == "__main__":
    pattern_sensor_oes = re.compile(r'^[0-9\.]{3,6}nm')
    row_max = 20
    r = 0
    flag_header = True
    with open(csvname) as f:
        reader = csv.reader(f)
        with open(csvname_2, 'w') as f2:
            writer = csv.writer(f2)
            list_header = list()
            for row in reader:
                if flag_header is True:
                    flag_header = False
                    for idx in range(len(row)):
                        element = row[idx]
                        if not pattern_sensor_oes.match(element):
                            list_header.append(idx)
                if r <= row_max:
                    row2 = [row[idx] for idx in list_header]
                    writer.writerow(row2)
                    r += 1
                else:
                    break
