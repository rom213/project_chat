from flask import Blueprint, request, jsonify
from flask_socketio import emit

sokets_bp = Blueprint('sokets', __name__)

buttons_state = {
    'security': False,
    'opendoor': False,
    'offlights': False,
    'alarm': False,
    'room': False,
    'dinning': False,
    'bathroom': False,
    'yarn': False
}


def register_socketio_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        emit('status_update', buttons_state)

    @socketio.on('toggle_button')
    def handle_toggle_button(data):
        button = data['button']
        buttons_state[button] = not buttons_state[button]
        emit('status_update', buttons_state, broadcast=True)

    
    @socketio.on('message')
    def handle_message(message):
        print("received message= " + message)
        if message != "User connected!":
            emit('message', message, broadcast=True)

