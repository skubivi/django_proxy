from rest_framework.response import Response
from rest_framework.views import APIView

import requests

main_server = 'https://armps2.invitro.ru'
test_server = 'http://10.10.10.199:8080'

server = False


# Create your views here.
def get_info(request):
    params = request.query_params.dict()
    headers = {}
    for key in request.META:
        if key[0:4] == 'HTTP':
            headers[key[5:].lower().replace('_', '-')] = request.META[key]
    body = request.data
    path = request.path
    return params, headers, body, path


class Request(APIView):
    def get(self, request):
        params, headers, _, path = get_info(request)
        global server
        if server is False:
            data = requests.request("GET", test_server + path, headers=headers, params=params)
        else:
            data = requests.request("GET", main_server + path, headers=headers, params=params)
        return Response(data.json())

    def post(self, request):
        params, headers, body, path = get_info(request)
        global server
        if server is False:
            data = requests.request("POST", test_server + path, headers=headers, params=params, json=body)
        else:
            data = requests.request("POST", main_server + path, headers=headers, params=params, json=body)
        return Response(data.json())

    def put(self, request):
        params, headers, body, path = get_info(request)
        global server
        if server is False:
            data = requests.request("PUT", test_server + path, headers=headers, params=params, data=body)
        else:
            data = requests.request("PUT", main_server + path, headers=headers, params=params, data=body)
        return Response(data.json())


class ChangeServer(APIView):
    def get(self, request):
        if server is False:
            return Response({'server': 'test', 'ip': test_server})
        return Response({'server': 'main', 'ip': main_server})

    def post(self, request):
        params, headers, _, _ = get_info(request)
        global server
        if params['server'] == 'test':
            server = False
            return Response({'server': 'test', 'ip': test_server})
        if params['server'] == 'main':
            server = True
            return Response({'server': 'main', 'ip': main_server})
        return Response({"status": "failure", "code": "400"}, status=400)
