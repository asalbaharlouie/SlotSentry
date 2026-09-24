from flask import Flask, jsonify, request

app = Flask(__name__)

state ={
    "watches": {},
    "current_id": 1
}

required_fields = ["title", "check_interval_minutes", "contact_email"]

@app.post("/watches")
def new_request():
    data = request.get_json()

    if not data:
        return jsonify({"response": "Invalid JSON"}), 400

    for info in required_fields:
        if info not in data:
            return jsonify({"response": f"Missing required field: {info}"}), 400

    watch_id = state["current_id"]

    state["watches"][watch_id] = {
        "id": watch_id,
        "status": "active",
        "title": data["title"],
        "check_interval_minutes": data["check_interval_minutes"],
        "contact_email": data["contact_email"]
    }

    state["current_id"] += 1

    response_data = {
        "id": watch_id,
        "status": "active",
        "title": data["title"],
        "check_interval_minutes": data["check_interval_minutes"],
        "contact_email": data["contact_email"]
    }

    return jsonify(response_data), 201

@app.get("/watches/<int:watch_id>")
def read_request(watch_id):

    if watch_id not in state["watches"]:
        return jsonify({"response": "Watch does not exist"}), 404

    watch = state["watches"][watch_id]

    return jsonify(watch), 200

@app.get("/watches")
def read_all_requests():

    all_watches = list(state["watches"].values())

    return jsonify(all_watches), 200

@app.patch("/watches/<int:watch_id>")
def update_request(watch_id):

    data = request.get_json()

    if watch_id not in state["watches"]:
        return jsonify({"response": "Watch does not exist"}), 404

    watch = state["watches"][watch_id]

    watch.update(data)

    return jsonify(watch),200

@app.delete("/watches/<int:watch_id>")
def delete_watch(watch_id):

    if watch_id not in state["watches"]:
        return jsonify({"response": "Watch does not exist"}), 404

    del state["watches"][watch_id]
    return "", 204

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)