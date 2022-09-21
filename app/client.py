import os
import grpc
import time

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path = dotenv_path)

import Detect_pb2
import Detect_pb2_grpc

GRPCPort = os.getenv("GRPCPort")
channel = grpc.insecure_channel(f"localhost:{GRPCPort}")
stub = Detect_pb2_grpc.DetectHandlerStub(channel)


LoopTime = "" 
CatchTime = ""

while True:
    LoopTime = str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
    if LoopTime != CatchTime:
        CatchTime = LoopTime
        pts = time.time()

        request = Detect_pb2.DetectRequest(Base64Image = "test.jpg")
        response = stub.YOLORDetector(request)

        time.sleep(0.01)
        pte = time.time()

        print("Time : " + str(float(pte - pts)))
        mytime = float(pte - pts)
        print(response.JsonString)
