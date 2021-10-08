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


f = open('/home/sun/Desktop/CRC/data/data.txt', 'w')

global_cnt = 0
# xlsx_list = glob.glob(SINGLE_DIR)
xlsx_list = glob.glob(MULTI_DIR)

len_list = []

for xlsx_idx, xlsx_file in enumerate(xlsx_list):

    for sheet_num in range(NUMOFSHEET):
        print("No {}-{}. {}".format(xlsx_idx, sheet_num, xlsx_file ))
        #print("No {}. {} {}".format(xlsx_idx, xlsx_file, sheet_num))
        # drop Header
        data = pd.read_excel(xlsx_file, sheet_name=sheet_num, header=None)

        # sliciing the data --> trash file exist
        data = data.loc[2:,:6]

        # drop the Nan
        data = data.dropna(axis=0)

        # DataFrame to numpy array
        numpy_data = data.to_numpy()

        print("numpy_data.shape : {}".format(numpy_data.shape))

        valid_data = []

        class_label = sheet_num

        for data_idx in range(len(numpy_data)):

            zero_start_flag = 0
            # first non zero
            non_zero_start_flag = 0
            # end non zero
            non_zero_end_flag = 0

            # instace list
            instance = []

            if numpy_data[data_idx][-1] == 0 and zero_start_flag == 0:
                zero_start_flag = 1

                instance.append(numpy_data[data_idx].tolist())

                for tmp_idx in range(data_idx+1, len(numpy_data)):
                    if non_zero_start_flag == 0 and zero_start_flag == 1 and numpy_data[tmp_idx][-1] == 0:
                        # print("continuous zero")
                        instance.append(numpy_data[tmp_idx].tolist())

                    elif non_zero_start_flag == 0 and zero_start_flag == 1 and numpy_data[tmp_idx][-1] != 0:
                        non_zero_start_flag = 1
                        instance.append(numpy_data[tmp_idx].tolist())

                    elif non_zero_start_flag and zero_start_flag and numpy_data[tmp_idx][-1] != 0:
                        instance.append(numpy_data[tmp_idx].tolist())

                    elif non_zero_start_flag and zero_start_flag and numpy_data[tmp_idx][-1] == 0:
                        instance.append(numpy_data[tmp_idx].tolist())
                        break
            if len(instance) > 8:
                if len(instance) > 30:
                    print(instance)
                f.write("{0:04}".format(global_cnt) + " {}\n".format(class_label))
                #np.save('/home/sun/Desktop/CRC/data/npy/{0:04}'.format(global_cnt), np.array(instance))
                global_cnt += 1

            #     print("* class label : ", class_label)
            #     print(instance)
            # # print(len(instance))
            # print(instance)


















        #
        #
        #
        #     del_cnt = 0
        #
        #     if  'X' in numpy_data[data_idx]:
        #         continue
        #     else:
        #         valid_data.append(list(numpy_data[data_idx]))
        #
        # valid_data = np.array(valid_data)
        #
        # print("valid_data.shape : {}".format(valid_data.shape))
        #
        # print(valid_data)

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
