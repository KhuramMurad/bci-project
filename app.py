from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import time
import threading
from digital_twin_bci import DigitalTwinBCI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-bci-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Digital Twin
twin = DigitalTwinBCI()
thread = None
thread_lock = threading.Lock()

def background_eeg_stream():
    """Background task to simulate streaming EEG data"""
    while True:
        # Generate new realistic EEG sample (8 channels)
        sample = twin.generate_realistic_eeg()
        
        # Prepare the data payload
        data_payload = {
            'timestamp': time.time(),
            'channels': sample.eeg
        }
        
        # Emit data to all connected clients on 'eeg_data' event
        socketio.emit('eeg_data', data_payload)
        
        # Sleep for 40ms to simulate ~25Hz refresh rate (to not overwhelm browser, though OpenBCI is often 250Hz)
        socketio.sleep(0.04)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_eeg_stream)
    print("Client connected")

@socketio.on('disconnect')
def test_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    # Start the server with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
