// import React, { useEffect, useState } from 'react';
// import './App.css';

// function App() {
//   const [message, setMessage] = useState('');

//   useEffect(() => {
//     fetch('http://localhost:8000/api/hello/')
//       .then(res => res.json())
//       .then(data => setMessage(data.message));
//   }, []);

//   return (
//     <div className="App">
//       <h1>{message}</h1>
//     </div>
//   );
// }

// export default App;

// frontend/src/App.js
import React from "react";
// import FirebaseCheck from "./components/FirebaseCheck";
import FirebaseCheck from "./components/firebaseCheck";

function App() {
  return (
    <div className="App">
      <FirebaseCheck />
    </div>
  );
}

export default App;
