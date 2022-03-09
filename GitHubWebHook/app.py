
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Testing GitHub WebHooks!"

@app.route('/apiGitHubWebHook/', methods=['POST'])
def GetDataFromGitHubWHooks():
    data = request.get_json()
    action = data['action']
    node_id = data['node_id']
    
    return jsonify(data)
    print(data)
    print(action)
    print(node_id)


#action = "created"
#repo_name = None
#nodeID = None

#if action in data
#run the script



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
