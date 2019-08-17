import logging
from get_answer.get_answer_pb2 import SearchResponse
from get_answer import get_answer_pb2_grpc


class GetAnswerServiceServicer(get_answer_pb2_grpc.GetAnswerServicer):
    """Provides methods that implement functionality of Search Service"""
    def __init__(self, grpc_server, search_service=None):
        logging.debug("GetAnswerService Started !")
        self.search_service = search_service
        get_answer_pb2_grpc.add_GetAnswerServicer_to_server(self, grpc_server)

    def _get_result_obj_from_tuple(self, query_result):

        return SearchResponse.Result(question=query_result[0], \
                                        answer=query_result[1], \
                                        similarity=query_result[2])

    def Search(self, request, context=None):

        """
        Searchest for nearest question present in db against the query
        """
        logging.debug(request.query)
        result = self.search_service.grpc_request(request.query)
        response = SearchResponse()
        response.result.extend(map(self._get_result_obj_from_tuple, result))
        return response
