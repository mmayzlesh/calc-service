from flask import Flask, request, jsonify, Response
import redis
import time
import os
import datetime
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
r = redis.Redis(host='redis-master', port=6379, decode_responses=True)  # Setting up Redis connection

# Setting up Prometheus counters for monitoring specific events in the application
API_ROOT_TIME_ACCESSED = Counter('api_root_time_accessed', 'Times the root endpoint returning local time in UTC format was accessed')
API_SUM_REQUESTED = Counter('api_sum_requested_total', 'Times the sum operation was requested')
API_DELETE_TRIGGERED = Counter('api_delete_triggered_total', 'Times a result was deleted')

@app.route('/', methods=['GET'])
def get_time():
    API_ROOT_TIME_ACCESSED.inc() # Increment the Prometheus counter for getting time
    # Return local machine time in UTC format
    return jsonify({"time": datetime.datetime.now(datetime.timezone.utc).isoformat()})

@app.route('/calculate', methods=['POST'])
def calculate():
    # Retrieve values from request and decide the operation
    num1, num2 = float(request.json.get('num1')), float(request.json.get('num2'))
    operation = request.json.get('operation')
    if operation in ['sum', '+']:
        result = num1 + num2
        API_SUM_REQUESTED.inc() # Increment the Prometheus counter for sum operations
    elif operation in ['product', '*']:
        result = num1 * num2
    else:
        return jsonify({'error': 'Invalid operation'}), 400

    # Store the result in Redis using current time as the key
    key = str(time.time())
    r.set(key, result)

    return jsonify({'result': result, 'key': key})

@app.route('/results', methods=['GET'])
def get_results():
    # Retrieve all calculations stored in Redis and return them
    keys = r.keys('*')
    results = {key: r.get(key) for key in keys}
    return jsonify(results)

@app.route('/results/<key>', methods=['DELETE'])
def delete_result(key):
    # Delete a specific result identified by its key
    if r.exists(key):
        r.delete(key)
        API_DELETE_TRIGGERED.inc() # Increment the Prometheus counter for delete operation
        return jsonify({'status': 'deleted'}), 200
    return jsonify({'error': 'Not found'}), 404

@app.route('/metrics', methods=['GET'])
def metrics():
    # Expose metrics for Prometheus to scrape
    return Response(generate_latest(), mimetype='text/plain')

@app.route('/readiness', methods=['GET'])
def readiness_check():
    try:
        # Try a simple Redis operation - this should return 'None' by Redis if it's up and running
        # If Redis is down, an error is expected.
        r.get('nonexistent_key')
        return jsonify({"status": "ready"}), 200
    except redis.RedisError:
        return jsonify({"status": "not-ready"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


# Run the Flask app if this script is the main entry point, e.g. using app.run()
# but if app is being served by other means, e.g. by Gunicorn etc., let them set the binding
if __name__ == "__main__":
    # Start the Flask application
    # Use the port specified by the 'PORT' environment variable, defaulting to 8080
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
