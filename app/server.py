import os
import time
import grpc 
from concurrent import futures

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path = dotenv_path)

import Detect_pb2
import Detect_pb2_grpc

import torch
from YOLOR.oop4yolor import OOP4YOLOR

yolor = OOP4YOLOR()
GRPCPort = os.getenv("GRPCPort")

class DetectHandler(Detect_pb2_grpc.DetectHandlerServicer):

    def YOLORDetector(self, request, context):
        response = Detect_pb2.DetectResponse()
        response.JsonString = MainFunction(request.Base64Image)
        return response

def MainFunction(Base64Image):
    # SaveFileName = f"{time.strftime('%Y%m%d%H%M%S', time.localtime())}.jpg"
    # try:
    #     ImageArray = base64.b64decode(Base64Image)
    #     ImageFile = np.fromstring(ImageArray, np.uint8) 
    #     img = cv2.imdecode(ImageFile, cv2.COLOR_BGR2RGB)  
    #     cv2.imwrite(f"static/tmp/{SaveFileName}", img)
    # except Exception as e:
    #     print(f"{e}")
    #     JsonString = "String is not base64 image"

    try:
        with torch.no_grad():
            JsonString = yolor.detect(Base64Image)
    except Exception as error:
        JsonString = error
    return str(JsonString)

def MainServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    Detect_pb2_grpc.add_DetectHandlerServicer_to_server(DetectHandler(), server)
    server.add_insecure_port('[::]:' + GRPCPort)
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    MainServer()
