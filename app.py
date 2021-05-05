#!/usr/bin/python
import psycopg2
from flask import Flask, request
from flask_restful import Api 
import json
from config import config
import uuid
import sys

app = Flask(__name__)
api = Api(app)


class userdata:

    def getuserjson(data):
        return{
            'user_id' : data[0],
            'firstname' : data[1],
            'lastname' : data[2],
            'username' : data[3],
            'gender' : data[4],
            'email_id' : data[5],
            'mobile' : data[6],
            'role_name' : data[9],
            'active' : data[10]
        }

    @app.route('/createuser', methods=['GET'])
    def create_user():
        try:
            # bar = request.args.to_dict()
            # print(bar)
            userid = request.args.get('userid',None)
            firstname = request.args.get('firstname',None)
            lastname = request.args.get('lastname',None)
            username = request.args.get('username',None)
            gender = request.args.get('gender',None)
            emailid = request.args.get('emailid',None)
            mobile = request.args.get('mobile',None)
            userrole = request.args.get('userrole',None)
            salt = request.args.get('salt',None)
            password = request.args.get('password',None)
            """ Connect to the PostgreSQL database server """
            conn = None
        
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            
            # create a cursor
            cur = conn.cursor()
            
            # makes entry for the newly created user
            cur.execute("""select INSERT_USER(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
            # (str(uuid.uuid4()),'test','4534535453','54543543545','2','test','test','1','test@test.com','9876543210'))
            (str(userid),username,salt,password,userrole,firstname,lastname,gender,emailid,mobile))
            data = cur.fetchall()
            conn.commit()

            if data is not None:
                response = data[0][0]
                if str(response) == '1':
                    return ({'statuscode' : 200, 'response' : 'user created successfully'})

            
            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            return ({"Exception type" : str(ex_type.__name__) , "Exception message" : str(ex_value)})
            # print('error : ',error.text)
            # return ({'error' : error.detail})
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    

    @app.route('/getuserdata', methods = ['GET'])
    def getuserdata():
        """ Connect to the PostgreSQL database server """
        userid = request.args.get('userid',None)
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            
            # create a cursor
            cur = conn.cursor()

            # makes entry for the newly created user
            cur.execute("""select * from userdata where user_id = \'%s\';""" % uuid.UUID(userid).hex)
            data = cur.fetchall()
            conn.commit()

            result= []

            for d in data:
                result.append(userdata.getuserjson(d))
            return ({'userdata' : result})

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('error : ',error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
    
    
    @app.route('/')
    def get_all():
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            
            # create a cursor
            cur = conn.cursor()

            result = []

            # makes entry for the newly created user
            cur.execute("""select * from userdata;""")
            data = cur.fetchall()
            conn.commit()

            for d in data:
                result.append(userdata.getuserjson(d))
            return ({'Users' : result})

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('error : ',error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

if __name__ == '__main__':
    app.run(debug=True)
    # userdata.getuserdata('b3962215-b8e0-4580-a284-902cb59a8761')
    # userdata.get_all()
    # userdata.create_user()