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
      {1 && <img className={style.image} src={"https://hips.hearstapps.com/hmg-prod/images/beautiful-smooth-haired-red-cat-lies-on-the-sofa-royalty-free-image-1678488026.jpg?crop=0.668xw:1.00xh;0.119xw,0&resize=1200:*"} alt="Received Image" />}
      {1 && <span className={style.result}>Healthy</span>}
    </div>
  );
};

export default App;