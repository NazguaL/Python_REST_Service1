#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import Response
import socket


db_connect = create_engine('sqlite:///chinook.db')
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
        print(ip)
        resourse = "http://" + ip + ":" + str(port) + "/calculator"
        return Response('{"data": "This is simple REST Calculator service working on %s"}' % resourse, status=200,
                        mimetype='application/json')


class Calculator(Resource):
    def get(self):
        print(ip)
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

        if operator == "Add":
            return {"result": int(opearand_1) + int(opearand_2)}
        elif operator == "Subtract)":
            return {"result": int(opearand_1) - int(opearand_2)}
        elif operator == "Multiply":
            return {"result": int(opearand_1) * int(opearand_2)}
        elif operator == "Divide":
            if opearand_2 != 0:
                return {"result": int(opearand_1) / int(opearand_2)}
            else:
                return Response('{"result": "Unable to divide by zero!"}', status=400, mimetype='application/json')
        else:
            return Response('{"result": "Empty or unsupported operator: %s"}' % operator, status=400,
                            mimetype='application/json')


class Employees(Resource):
    def get(self):
        print(request.json)
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
    
    def post(self):
        conn = db_connect.connect()
        for i in request.json:
            print(request.json[i])
        LastName = request.json['LastName']
        FirstName = request.json['FirstName']
        Title = request.json['Title']
        ReportsTo = request.json['ReportsTo']
        BirthDate = request.json['BirthDate']
        HireDate = request.json['HireDate']
        Address = request.json['Address']
        City = request.json['City']
        State = request.json['State']
        Country = request.json['Country']
        PostalCode = request.json['PostalCode']
        Phone = request.json['Phone']
        Fax = request.json['Fax']
        Email = request.json['Email']
        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}', \
                             '{13}')".format(LastName,FirstName,Title,
                             ReportsTo, BirthDate, HireDate, Address,
                             City, State, Country, PostalCode, Phone, Fax,
                             Email))
        return {'status':'success'}

    
class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    
class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Root, '/')  # Route_0
api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_2.
api.add_resource(Calculator, '/calculator')  # Route_3


if __name__ == '__main__':
    app.run(host=ip, port=port)
