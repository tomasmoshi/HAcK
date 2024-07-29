import React, { useState, useEffect } from "react";
import io from 'socket.io-client';

const socket = io('http://localhost:8000');

function App() {
  const [temp, setTemp] = useState(null);
  const [ultrasonic, setUltrasonic] = useState(null);
  const [humidity, setHumidity] = useState(null);

  useEffect(() => {
    socket.on('temp', setTemp);
    socket.on('distance', setUltrasonic);
    socket.on('humidity', setHumidity);

    const handleKeyDown = (event) => {
      switch (event.key) {
        case 'w':
          sendDirection('forward');
          break;
        case 'a':
          sendDirection('left');
          break;
        case 's':
          sendDirection('backward');
          break;
        case 'd':
          sendDirection('right');
          break;
        default:
          break;
      }
    };

    const handleKeyUp = (event) => {
      if (['w', 'a', 's', 'd'].includes(event.key)) {
        sendDirection('stop');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      socket.off('temp', setTemp);
      socket.off('ultrasonic', setUltrasonic);
      socket.off('humidity', setHumidity);
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  const sendDirection = (direction) => {
    socket.emit('send-direction', direction);
  };

  const sendArmValue = (value) => {
    socket.emit('send-arm-value', value);
  };

  const sendPinchValue = (value) => {
    socket.emit('send-pinch-value', value);
  };

  const sendGrab = () => {
    socket.emit('send-arm-command', 'grab');
  };

  const sendRelease = () => {
    socket.emit('send-arm-command', 'release');
  };

  return (
    <div className="App">
      <h1>Rover Control</h1>
      <div>
        <button onClick={() => sendDirection('forward')}>Forward</button>
        <button onClick={() => sendDirection('backward')}>Backward</button>
        <button onClick={() => sendDirection('left')}>Left</button>
        <button onClick={() => sendDirection('right')}>Right</button>
        <button onClick={() => sendDirection('stop')}>Stop</button>
      </div>
      <div>
        <button onClick={sendGrab}>Grab</button>
        <button onClick={sendRelease}>Release</button>
      </div>
      <div>
        <input
          type="number"
          placeholder="Arm Value"
          onChange={(e) => sendArmValue(e.target.value)}
        />
      </div>
      <div>
        <input
          type="number"
          placeholder="Pinch Value"
          onChange={(e) => sendPinchValue(e.target.value)}
        />
      </div>
      <div>
        <h2>Sensor Data</h2>
        <p>Temperature: {temp}</p>
        <p>Ultrasonic: {ultrasonic}</p>
        <p>Humidity: {humidity}</p>
      </div>
    </div>
  );
}

export default App;
