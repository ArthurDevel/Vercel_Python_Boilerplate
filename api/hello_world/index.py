from flask import Blueprint, jsonify, request
from typing import Dict

hello_world_bp = Blueprint('hello_world', __name__, url_prefix='/api/hello_world')

@hello_world_bp.route('/get_hello_world', methods=['GET'])
def get_hello_world() -> Dict:
    return handle_get_hello_world()

@hello_world_bp.route('/post_hello_world', methods=['POST'])
def post_hello_world() -> Dict:
    args = request.get_json()
    return handle_post_hello_world(args)

def handle_get_hello_world() -> Dict:
    """
    Handler for the GET hello world request.
    
    Returns:
        Dict: A greeting message and status code
    """
    return {
        "message": "Hello, World!",
        "status_code": 200
    }

def handle_post_hello_world(args: Dict) -> Dict:
    """
    Handler for the POST hello world request.
    
    Args:
        args (Dict): The input parameters containing name
    
    Returns:
        Dict: A personalized greeting message and status code
    """
    if not args or 'name' not in args:
        return {
            "error": "Please provide a name in the request body",
            "status_code": 400
        }
    
    name = args['name']
    return {
        "message": f"Hello, {name}!",
        "status_code": 200
    }

if __name__ == "__main__":
    # Test requests
    print("Testing GET endpoint:", handle_get_hello_world())
    
    test_post = {"name": "Alice"}
    print("Testing POST endpoint:", handle_post_hello_world(test_post))
    