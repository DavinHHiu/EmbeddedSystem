import React, { useEffect, useState } from 'react';
import { w3cwebsocket as WebSocketClient } from 'websocket';
import axios from 'axios';
import style from './App.module.scss';

const App = () => {
  const [imageSrc, setImageSrc] = useState('');
  const [result, setResult] = useState(null);

  useEffect(() => {
    const ws = new WebSocketClient('ws://192.168.1.27:60');

    ws.onmessage = (event) => {
      const imageData = event.data;

      const data = {
        'image': imageData
      }

      axios.post("http://localhost:8000", data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then((response) => {
          if (response.status === 200) {
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
    <div className={style.container}>
      <h1 className={style.title}>TOMATO DETECTOR</h1>
      {imageSrc && <img className={style.image} src={imageSrc} alt="Received Image" />}
      {result && <span className={style.result}>{result}</span>}
    </div>
  );
};

export default App;