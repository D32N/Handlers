from flask import Flask, jsonify, request, abort
import os, json, pymongo

app = Flask(__name__)

## Connect to MongoDB
print "\n## Establish the connection and aim at a specific database"
##if 'VCAP_SERVICES' in os.environ:
##        VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
##        MONCRED = VCAP_SERVICES["mlab"][0]["credentials"]
##        client = pymongo.MongoClient(MONCRED["uri"])
##        DB_NAME = str(MONCRED["uri"].split("/")[-1])
##else:
##        client = pymongo.MongoClient('192.168.26.130:27017')
##        DB_NAME = "HandlersDB"
client = pymongo.MongoClient('192.168.26.130:27017')
DB_NAME = "HandlersDB"

print "Connecting to database : " + DB_NAME

## Connect to database
db = client[DB_NAME]

## [C]RUD
@app.route('/api/v1/create', methods=["POST"])
def create():
        print("FUNCTION: CREATE/PUT")
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

@app.route('/foo', methods=['POST']) 
def foo():
    if not request.json:
        abort(400)
    print request.json
    return json.dumps(request.json)

## C[R]UD
@app.route('/api/v1/read', methods=["GET"])
def read():
        req = request.args
        ## Put all passed parameters in a dictionary
        ## Remember that input received is type string...
        ## cast to int for the search against MongoDB document
        ## The alternative is to have all fields as string in MongoDB
        ## Which we're trying  now... changed MongoDB id data type to string
        #h_id = int(req['h_id'])
        #print(str(h_id))

        h_id = req['h_id']
        print(h_id)

        handler_details = db.handlers.find_one({'h_id': h_id})
        #print handler_details
        ## It looks like MongoDB only returns UTF8...??? *sigh*
        h_name = handler_details[u'h_name']
        h_picture = handler_details[u'h_picture']
        h_servicedogid = handler_details[u'h_servicedogid']
        h_trainerorg = handler_details[u'h_trainerorg']
        print(h_id, h_name, h_picture, h_servicedogid, h_trainerorg)

        handler = {'h_id': h_id, 'h_name': h_name, 'h_picture': h_picture, 'h_servicedogid': h_servicedogid, 'h_trainerorg': h_trainerorg}
        return jsonify(handler)
        
if __name__ == "__main__":
        app.run(debug=False, host='127.0.0.1', port=int(os.getenv('PORT', '5002')))
