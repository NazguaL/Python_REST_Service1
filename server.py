#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import Response
import socket


db_connect = create_engine('sqlite:///logdb.db')
app = Flask(__name__)
api = Api(app)
port = 5002


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


ip = get_ip_address()
print("http://" + ip + ":" + str(port))


class Root(Resource):
    def get(self):
        print(str(request.remote_addr))
        resourse = "http://" + ip + ":" + str(port) + "/calculator"
        return Response('{"data": "This is simple REST Calculator service working on %s"}' % resourse, status=200,
                        mimetype='application/json')


class Logs(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select id, result from log;")
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class LogsId(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select id, Operand1, Operand2, operator, result from log where id =%s " % int(id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


class Calculator(Resource):
    def get(self):

        instruction = "To use this Calculator service call POST method on this resource address using JSON with " \
                      "following keys Operand#1, Operand#2 and Operator in Request body " \
                      "and Content-Type application/json header"
        return Response('{"instructions": "%s"}' % instruction, status=200, mimetype='application/json')

    def post(self):

        for i in request.json:
            print(request.json[i])

        operator = request.json['Operator']
        opearand_1 = request.json['Operand#1']
        opearand_2 = request.json['Operand#2']
        conn = db_connect.connect()
        status = 200

        if operator == "Add":
            result = float(opearand_1) + float(opearand_2)
        elif operator == "Subtract)":
            result = float(opearand_1) - float(opearand_2)
        elif operator == "Multiply":
            result = float(opearand_1) * float(opearand_2)
        elif operator == "Divide":
            if opearand_2 != 0:
                result = float(opearand_1) / float(opearand_2)
            else:
                result = "Unable to divide by zero!"
                status = 400
        else:
            result = "Empty or unsupported operator: %s" % operator
            status = 400
        query = conn.execute("insert into log values(null,'{0}','{1}','{2}','{3}')".format(opearand_1, opearand_2, operator, result))
        return Response('{"result": "%s"}' % result, status=status, mimetype='application/json')


api.add_resource(Root, '/')  # Route_0
api.add_resource(Logs, '/calculator/logs')  # Route_1
api.add_resource(LogsId, '/calculator/logs/<id>')  # Route_2
api.add_resource(Calculator, '/calculator')  # Route_3


if __name__ == '__main__':
    app.run(host=ip, port=port)
