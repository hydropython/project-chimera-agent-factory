"""Minimal mock OpenClaw server for local integration tests.

Endpoints implemented:
- POST /api/agents/register
- POST /api/services/register
- POST /api/trends/fetch

Run: python tests/mock_openclaw.py
"""
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/api/agents/register', methods=['POST'])
def register_agent():
    body = request.get_json(force=True)
    # Simple validation
    if 'agent_id' not in body or 'public_key' not in body:
        return jsonify({
            'error': 'invalid_payload',
            'message': "Missing 'agent_id' or 'public_key'"
        }), 400
    return jsonify({'agent_status': 'registered', 'agent_id': body.get('agent_id')}), 201

@app.route('/api/services/register', methods=['POST'])
def register_service():
    body = request.get_json(force=True)
    if 'service_id' not in body or 'agent_id' not in body or 'endpoint' not in body:
        return jsonify({'error': 'invalid_payload','message': "Missing required fields"}), 400
    return jsonify({'service_status': 'registered', 'service_id': body.get('service_id')}), 201

@app.route('/api/trends/fetch', methods=['POST'])
def fetch_trends():
    body = request.get_json(force=True)
    request_id = body.get('request_id', f'req_{int(time.time())}')
    # Return a small example response
    resp = {
        'request_id': request_id,
        'status': 'success',
        'data': {
            'trends': [
                {
                    'id': 'trend_001',
                    'source': 'twitter',
                    'title': 'AI Breakthrough',
                    'volume': 15000,
                    'sentiment': 0.72,
                    'categories': ['technology','innovation']
                }
            ]
        }
    }
    return jsonify(resp), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
