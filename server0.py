from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import urllib.parse as urlparse

import torch
import torch.nn.functional as F
from tools.model import Net, Net2
import numpy as np

host = '203.246.113.83' # 호스트 ip를 적어주세요
port = 8080            # 포트번호를 임의로 설정해주세요

reset_flag = False

call_back_counter = 0
valid_call_back_counter = 0

data_list = []

pre_result = -1

idx_to_label = {
    0 : '-',
    1 : 'ㄱ',
    2 : 'ㄹ',
    3 : 'ㅁ',
    4 : 'ㅂ',
    5 : 'ㅅ',
    6 : 'ㅇ',
    7 : 'ㅈ',
    8 : 'ㅊ',
    9 : 'ㅋ',
    10 : 'ㅎ',
    11 : 'ㅏ',
    12 : 'ㅣ',
}

multi_motion_cnt = [
    0, # 감사
    0, # 길
    0, # 마차
    0, # 비
    0, # 바람
    0, # 방
    0, # 사람
    0, # 사랑
    0, # 새
    0, # 입
    0, # 집
    0, # 차
    0, # 치마
    0, # 키
    0, # 하지
    0  # 해
]

SINGLE_GESTURE = [
    [1,1,1,1,1], # -
    [1,1,0,0,0], # ㄱ
    [0,1,1,1,0], # ㄹ
    [0,0,0,0,0], # ㅁ
    [0,1,1,1,1], # ㅂ
    [0,1,1,0,0], # ㅅ
    [0,0,1,1,1], # ㅇ
    [1,1,1,0,0], # ㅈ
    [1,1,1,1,0], # ㅊ
    [1,0,1,0,0], # ㅋ
    [1,0,0,0,0], # ㅎ
    [0,1,0,0,0], # ㅏ
    [0,0,0,0,1], # ㅣ
]

def data_to_gesture(np_data):
    global SINGLE_GESTURE

    return_single_class = -1

    list_data = [0,0,0,0,0]

    for np_idx in range(len(np_data)):
        if np_data[np_idx] >= 0.0:
            list_data[np_idx] = 1
        elif np_data[np_idx] < 0.0:
            list_data[np_idx] = 0
        # else:
        #     list_data[np_idx] = 2

    for sg_idx in range(len(SINGLE_GESTURE)):
        if SINGLE_GESTURE[sg_idx] == list_data:
            return_single_class = sg_idx
            break

    return return_single_class



def make_data(infer_data):
    x_min = 650.0
    x_max = 4000.0

    gesture_data = np.array(infer_data, np.float)
    # normalize
    gesture_data = (gesture_data - x_min) / (x_max - x_min)

    # gesture_data = gesture_data * 2.0 - 1.0

    if len(gesture_data) <= 30:
        gesture_data = np.append(gesture_data, np.zeros((30-len(gesture_data), 5)), axis=0)

    torch_data = torch.from_numpy(gesture_data)

    torch_data = torch.reshape(torch_data, (1,1,30,5))

    # print(torch_data)

    return torch_data

def model_run(infer_data):

    torch_data = make_data(infer_data)

    model = Net2()

    state_dict_path = "/home/sun/Desktop/CRC/output/new_model/90_state_dict_model.pt"
    # state_dict_path = "/home/sun/Desktop/CRC/output/model1/28_state_dict_model.pt"

    model.load_state_dict(torch.load(state_dict_path))

    model = model.cuda()

    model.eval()

    torch_data = torch_data.cuda().float()

    pred = model(torch_data)

    # print("prediction : ", pred)

    class_idx = torch.argmax(pred, 1)

    return int(class_idx.item()), pred.cpu()


class RequestHandler(BaseHTTPRequestHandler):
    def __get_Post_Parameter(self, key):
        # 해당 클래스에 __post_param변수가 선언되었는지 확인한다.
        if hasattr(self,"_myHandler__post_param") == False:
            # 해더로 부터 formdata를 가져온다.
            data = self.rfile.read(int(self.headers['Content-Length']));
            if data is not None:
                self.__post_param = dict(urlparse.parse_qs(data.decode()));
            else :
                self.__post_param = {};
        if key in self.__post_param:

            return self.__post_param['start'][0], self.__post_param['end'][0];
        return None;

    def __set_Header(self, code):
        self.send_response(code);
        self.send_header('Content-type','application/json');
        self.end_headers();

    # http 프로토콜의 body내용을 넣는다.
    def __set_response(self, data):
        global call_back_counter
        global valid_call_back_counter
        global data_list
        global pre_result
        global reset_flag
        global multi_motion_cnt

        if(data):
            call_back_counter += 1

            # print("data : ", data)

            check_header=data[0].split(" ")[0]
            end_flag = data[1]

            print(check_header)
            print(end_flag)

            if(check_header=="#" and end_flag == "false"):
                # x_min = 650.0
                # x_max = 4000.0
                x_min = 750.0
                x_max = 3900.0


                reset_flag = False
                print("reset_flag : ################## ")

                valid_call_back_counter += 1

                raw_data=data[0][1:30]
                split_data = raw_data.split(" ")

                # if !split_data[1].isdigit():
                #    print("Unknown Data")
                #    continue

                print(split_data)
                for sp_idx in range(len(split_data)):
                    if '\r' in split_data[sp_idx]:
                        split_data[sp_idx] = split_data[sp_idx].replace('\r', '')




                float_data = [float(i) for i in split_data if i.isdigit()]

                numpy_float_data = np.array(float_data)
                numpy_float_data[3] -= 500.0

                print(numpy_float_data)

                numpy_float_data = (numpy_float_data - x_min) / (x_max - x_min)

                numpy_float_data = numpy_float_data*2 - 1

                print(numpy_float_data)

                single_class_idx = data_to_gesture(numpy_float_data)

                print("single_class_idx : ", single_class_idx)
                #print(idx_to_label[single_class_idx])

                if single_class_idx == 1:
                    multi_motion_cnt[0] += 1
                    multi_motion_cnt[1] += 1
                if single_class_idx == 2:
                    multi_motion_cnt[1] += 1
                    multi_motion_cnt[4] += 1
                    multi_motion_cnt[6] += 1
                    multi_motion_cnt[7] += 1
                if single_class_idx == 3:
                    multi_motion_cnt[0] += 1
                    multi_motion_cnt[2] += 1
                    multi_motion_cnt[4] += 1
                    multi_motion_cnt[6] += 1
                    multi_motion_cnt[12] += 1
                if single_class_idx == 4:
                    multi_motion_cnt[4] += 1
                    multi_motion_cnt[5] += 1
                    multi_motion_cnt[9] += 1
                    multi_motion_cnt[10] += 1
                if single_class_idx == 5:
                    multi_motion_cnt[0] += 1
                    multi_motion_cnt[6] += 1
                    multi_motion_cnt[7] += 1
                    multi_motion_cnt[8] += 1
                if single_class_idx == 6:
                    multi_motion_cnt[5] += 1
                    multi_motion_cnt[7] += 1
                    multi_motion_cnt[9] += 1
                if single_class_idx == 7:
                    multi_motion_cnt[10] += 1
                if single_class_idx == 8:
                    #multi_motion_cnt[11] += 1
                    multi_motion_cnt[12] += 1
                #if single_class_idx == 9:
                    #multi_motion_cnt[13] += 1
                if single_class_idx == 10:
                    multi_motion_cnt[14] += 1
                    #multi_motion_cnt[15] += 1
                if single_class_idx == 11:
                    multi_motion_cnt[0] += 1
                    multi_motion_cnt[2] += 1
                    multi_motion_cnt[4] += 1
                    multi_motion_cnt[5] += 1
                    multi_motion_cnt[6] += 1
                    multi_motion_cnt[7] += 1
                    multi_motion_cnt[8] += 1
                    multi_motion_cnt[9] += 1
                    #multi_motion_cnt[11] += 1
                    multi_motion_cnt[12] += 1
                    multi_motion_cnt[14] += 1
                    #multi_motion_cnt[15] += 1
                if single_class_idx == 12:
                    multi_motion_cnt[1] += 1
                    multi_motion_cnt[3] += 1
                    multi_motion_cnt[8] += 1
                    multi_motion_cnt[9] += 1
                    multi_motion_cnt[10] += 1
                    multi_motion_cnt[12] += 1
                    #multi_motion_cnt[13] += 1
                    multi_motion_cnt[14] += 1
                    #multi_motion_cnt[15] += 1

                if len(float_data) == 5:
                    data_list.append(float_data)

                test={"class":"-1", "endclass":"0"}
                self._send_class(test)

            elif(check_header=="#" and end_flag == "true"):
                print("어미!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                x_min = 650.0
                x_max = 3900.0

                reset_flag = False
                print("reset_flag : ################## ")

                valid_call_back_counter += 1

                raw_data=data[0][1:30]
                split_data = raw_data.split(" ")

                # if !split_data[1].isdigit():
                #    print("Unknown Data")
                #    continue

                print(split_data)
                for sp_idx in range(len(split_data)):
                    if '\r' in split_data[sp_idx]:
                        split_data[sp_idx] = split_data[sp_idx].replace('\r', '')




                float_data = [float(i) for i in split_data if i.isdigit()]

                numpy_float_data = np.array(float_data)

                print(numpy_float_data)

                numpy_float_data = (numpy_float_data - x_min) / (x_max - x_min)

                numpy_float_data = numpy_float_data*2 - 1

                print(numpy_float_data)

                single_class_idx = data_to_gesture(numpy_float_data)

                print("single_class_idx : ", single_class_idx)
                #print(idx_to_label[single_class_idx])

                if single_class_idx == 8:
                    multi_motion_cnt[11] += 1
                    # multi_motion_cnt[12] += 1
                if single_class_idx == 9:
                    multi_motion_cnt[13] += 1
                if single_class_idx == 10:
                    # multi_motion_cnt[14] += 1
                    multi_motion_cnt[15] += 1


                if len(float_data) == 5:
                    data_list.append(float_data)

                test={"class":str(pre_result), "endclass":"1"}
                self._send_class(test)

            elif(check_header=="*"):
                reset_flag = True
                print("reset_flag : ************************* ")

                test_flag = 9

                if len(data_list):
                    # calc data_list
                    if len(data_list) > 30:
                        data_list = data_list[:30]
                    class_idx, pred = model_run(data_list)
                    pred = F.softmax(pred,dim=1)
                    print("prediction : ", pred)
                    if class_idx == test_flag:
                        print("Correct")
                    else:
                        print("Fail")

                    # class_idx = test_flag
                    torch_multi_motion_pred = pred[0].detach().numpy()
                    print("multi_motion_cnt : ", multi_motion_cnt)

                    np_multi_motion_cnt = np.array(multi_motion_cnt)

                    np_max = np.max(np_multi_motion_cnt)

                    for np_idx in range(len(np_multi_motion_cnt)):
                        if np_multi_motion_cnt[np_idx] == np_max:
                            np_multi_motion_cnt[np_idx] = 1
                        else:
                            np_multi_motion_cnt[np_idx] = 0



                    class_idx = np.argmax(np_multi_motion_cnt*torch_multi_motion_pred)

                    class_idx += 1

                    # return_class_idx = None
                    #
                    # if class_idx == 12:
                    #     return_class_idx = str(pre_result) + 'a'
                    # elif class_idx == 14:
                    #     return_class_idx = str(pre_result) + 'b'
                    # elif class_idx == 16:
                    #     return_class_idx = str(pre_result) + 'c'


                    print("class_idx : ", class_idx)
                    # class_idx = 1
                    # if end_flag == "false":
                    #     pre_result = return_class_idx
                    # pre_result = 0

                    test = {"class":str(class_idx), "endclass":"0"}
                    self._send_class(test)
                else:
                    test = {"class":pre_result, "endclass":"0"}
                    self._send_class(test)


                # test={"class":"12"}
                # self._send_class(test)
                # print("data_list : ", data_list)

            else:
                print("None")
                test={"class":"-1"}
                self._send_class(test)
        else:
            print("Wrong data")

        if reset_flag:
            data_list = []
            call_back_counter = 0
            valid_call_back_counter = 0
            multi_motion_cnt = [
                0, # 감사
                0, # 길
                0, # 마차
                0, # 비
                0, # 바람
                0, # 방
                0, # 사람
                0, # 사랑
                0, # 새
                0, # 입
                0, # 집
                0, # 차
                0, # 치마
                0, # 키
                0, # 하지
                0  # 해
            ]

        print("call_back_counter : " ,call_back_counter)
        print("valid_call_back_counter : " ,valid_call_back_counter)



    def _send_class(self,dict):
        self.send_response(200)
        #self.send_header("Content-Type","application/json")
        #self.end_headers()
        # send _json
        self.wfile.write(bytes(json.dumps(dict),"utf8"))


    def do_POST(self):
        self.__set_Header(200);
        self.__set_response(self.__get_Post_Parameter('start'));









if __name__=="__main__":
    httpd=HTTPServer((host,port),RequestHandler)
    print("Hosting Server on port 8080")
    httpd.serve_forever()
