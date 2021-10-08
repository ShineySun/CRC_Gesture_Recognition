from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import urllib.parse as urlparse

host = '203.246.113.83' # 호스트 ip를 적어주세요
port = 8080            # 포트번호를 임의로 설정해주세요


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

            return self.__post_param[key][0];
        return None;
    def __set_Header(self, code):
        self.send_response(code);
        self.send_header('Content-type','application/json');
        self.end_headers();

    # http 프로토콜의 body내용을 넣는다.

    def __set_response(self, data):

        if(data):
            check_header=data.split(" ")[0]
            if(check_header=="#"):

                row_data=data[1:30]
                print(row_data)
                send_data={"class",int(1)}
                json_data=json.dumps(send_data)
                headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
                res = requests.post(url, params={'result':data}, verify=False , headers=headers)

            else:
                # end 할 때
                print("*")


        else:
            print("Wrong data")






    def do_POST(self):
        self.__set_Header(200);
        self.__set_response(self.__get_Post_Parameter('start'));









if __name__=="__main__":
    httpd=HTTPServer((host,port),RequestHandler)
    print("Hosting Server on port 8080")
    httpd.serve_forever()
