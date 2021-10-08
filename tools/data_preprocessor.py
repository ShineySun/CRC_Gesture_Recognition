# PATH
import os
import glob

# READ DATA
import pandas as pd
import numpy as np

# Check existance of 'X'
def is_exist_X(test_data):
    for test_idx in range(len(test_data)):
        if 'X' in test_data[test_idx]:
            return False
    return True

# 단일 데이터
# SINGLE_DIR = r'/home/sun/Desktop/CRC/Single_Motion/**/**/단일/*.xlsx'
MULTI_DIR = r'/home/sun/Desktop/CRC/Multi_Motion/**/**/연속/*.xlsx'
# Number of Sheet
NUMOFSHEET = 16

# xlsx_list = glob.glob(SINGLE_DIR)
xlsx_list = glob.glob(MULTI_DIR)

for xlsx_idx, xlsx_file in enumerate(xlsx_list):

    for sheet_num in range(NUMOFSHEET):
        print("No {}-{}. {}".format(xlsx_idx, sheet_num, xlsx_file ))
        #print("No {}. {} {}".format(xlsx_idx, xlsx_file, sheet_num))
        # drop Header
        data = pd.read_excel(xlsx_file, sheet_name=sheet_num, header=None)

        # sliciing the data --> trash file exist
        data = data.loc[4:,:6]

        # drop the Nan
        data = data.dropna(axis=0)

        # DataFrame to numpy array
        numpy_data = data.to_numpy()

        print("numpy_data.shape : {}".format(numpy_data.shape))

        valid_data = []

        for data_idx in range(len(numpy_data)):
            del_cnt = 0

            if  'X' in numpy_data[data_idx]:
                continue
            else:
                valid_data.append(list(numpy_data[data_idx]))

        valid_data = np.array(valid_data)

        print("valid_data.shape : {}".format(valid_data.shape))

        print(valid_data)

        #print(is_exist_X(valid_data))

        #if is_exist_y\

                #del_cnt += 1
                #print(del_cnt)

        # print(is_exist_X(valid_data))

        # numpy_data = data.to_numpy()

        # drop the NAN Column
        #numpy_data = numpy_data[np.logical_not(np.isnan(numpy_data))]

        #print(numpy_data)
        #

        # if numpy_data.shape[1] != 7:
        #     print("No {}-{}. {}".format(xlsx_idx, sheet_num, xlsx_file ))
        #     print(numpy_data.shape)
        #     print(numpy_data)
