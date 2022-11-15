from flask import Flask, request

app = Flask(__name__)

@app.get('/api')
def fetcher():
    print(request.args.to_dict())
    return {"recommendation_1":"rice","recommendation_2":"wheat","recommendation_3":"maize"}

app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)