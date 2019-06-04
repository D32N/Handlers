##Create - request.json
##Read - request.args
##Update - request.json
##Delete - request.form

from flask import Flask, jsonify, request, abort
import os, json, pymongo

app = Flask(__name__)

## Connect to MongoDB
print "\n## Establish the connection and aim at a specific database"
if 'VCAP_SERVICES' in os.environ:
        VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
        MONCRED = VCAP_SERVICES["mlab"][0]["credentials"]
        client = pymongo.MongoClient(MONCRED["uri"])
        DB_NAME = str(MONCRED["uri"].split("/")[-1])
else:
        client = pymongo.MongoClient('192.168.26.130:27017')
        DB_NAME = "HandlersDB"

## Connect to DB instance
db = client[DB_NAME]

## [C]rud
@app.route('/api/v1/create', methods=["POST"])
def create():
        print("FUNCTION: CREATE/POST")
        if not request.json:
                abort(400)

        data = request.json

        h_id = data['h_id']
        h_name = data['h_name']
        h_picture = data['h_picture']
        h_servicedogid = data['h_servicedogid']
        h_trainerorg = data['h_trainerorg']

        h_exists = db.handlers.find_one({'h_id': h_id})
        if not h_exists:
                db.handlers.insert_one({'h_id': h_id, 'h_name': h_name, 'h_picture': h_picture, 'h_servicedogid': h_servicedogid, 'h_trainerorg': h_trainerorg})
                response = {'status': "Handler added", 'code': 100}
        else:
                response = {'status': "Handler ID already exists, request not processed", 'code': 101}
        return jsonify(response)

## c[R]ud
@app.route('/api/v1/read', methods=["GET"])
def read():
        print("FUNCTION: READ/GET")
        
        data = request.args
        h_id = data['h_id']

        h_exists = db.handlers.find_one({'h_id': h_id})
        if h_exists:
                h_name = h_exists[u'h_name']
                h_picture = h_exists[u'h_picture']
                h_servicedogid = h_exists[u'h_servicedogid']
                h_trainerorg = h_exists[u'h_trainerorg']
                print(h_id, h_name, h_picture, h_servicedogid, h_trainerorg)
                response = {'h_id': h_id, 'h_name': h_name, 'h_picture': h_picture, 'h_servicedogid': h_servicedogid, 'h_trainerorg': h_trainerorg}
        else:
                response = {'status': "Handler does not exist", 'code': 101}
        return jsonify(response)

## cr[U]d
@app.route('/api/v1/update', methods=["PUT"])
def update():
        print("FUNCTION: UPDATE/PUT")
        if not request.json:
                abort(400)

        data = request.json
        h_id = data['h_id']

        ## Check for hander ID exists in MongoDB HandersDB
        hid_exists = db.handlers.find_one({'h_id': h_id})
        if hid_exists:

        ## Work on the keys in json input
                for hattrib in data:
                        ## Check to see whether the attribute we're working on is h_id
                        ## h_id may not be modified, all other attribs may be modified
                        if hattrib != "h_id":
                                ## Modify the attribute
                                db.handlers.find_one_and_update({'h_id': h_id},
                                                                {"$set": {hattrib: data[hattrib]}})
                if len(data) == 2:
                        response = {'status': "Handler ID found, attribute updated", 'code': 100}
                else:
                        response = {'status': "Handler ID found, attributes updated", 'code': 100}
                        
        else:
                response = {'status': "Handler ID not found, attributes could not be updated", 'code': 101}
        return jsonify(response)

## cru[D]
@app.route('/api/v1/delete', methods=["DELETE"])
def delete():
        print("FUNCTION: DELETE/DELETE")

        data = request.args
        h_id = data['h_id']

        hid_exists = db.handlers.find_one({'h_id': h_id})
        if hid_exists:
                db.handlers.delete_one({'h_id': h_id})
                response = {'status': "Handler deleted", 'code': 100}
        else:
                response = {'status': "Handler ID not found, no delete operation performed", 'code': 101}
        return jsonify(response)
        
if __name__ == "__main__":
        app.run(debug=False, host='127.0.0.1', port=int(os.getenv('PORT', '5000')), threaded=True)
