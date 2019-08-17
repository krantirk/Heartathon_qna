import grpc


from concurrent import futures
import os
import time
import json
import logging

from qna.src.analysis import Analysis
from get_answer.get_answer_service_grpc import GetAnswerServiceServicer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

qna_data_path = "./qna/data/kg"
question_template_path = "./qna/data/question_templates.csv"

config = {
    "service_port": 9090,
    "qna_data_path": "./qna/data/kg",
    "question_template_path": "./qna/data/question_templates.csv"

}

def serve():
    # with open(os.path.abspath('heartsapp/config.json'), 'r') as f:
    #     config = json.load(f)
    service_port = config['service_port']

    # Init GRPC Server
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Init GRPC Services
    get_answer = Analysis(config["qna_data_path"], config["question_template_path"])
    GetAnswerServiceServicer(grpc_server, get_answer)

    # Start Server
    grpc_server.add_insecure_port('[::]:' + str(service_port))
    grpc_server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	serve()
