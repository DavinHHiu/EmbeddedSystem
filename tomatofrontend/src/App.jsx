import React, { useEffect, useState } from 'react';
import { w3cwebsocket as WebSocketClient } from 'websocket';
import axios from 'axios';

const App = () => {
  const [imageSrc, setImageSrc] = useState('');
  const [result, setResult] = useState(null);

  useEffect(() => {
    const ws = new WebSocketClient('ws://192.168.1.27:60');

    ws.onmessage = (event) => {
      const imageData = event.data;
      // console.log('Received image data:', imageData);

      const data = {
        'image': imageData
      }

      axios.post("http://localhost:8000", data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then((response) => {
          // console.log(response);
          if (response.status === 200) {
            console.log(response.data.result)
            setResult(response.data.result)
          }
        });

      const imageUrl = URL.createObjectURL(imageData);
      setImageSrc(imageUrl);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div>
      <h1>Arduino Image Viewer</h1>
      {imageSrc && <img src={imageSrc} alt="Received Image" />}
      {result && <span>{result}</span>}
    </div>
  );
};

export default App;