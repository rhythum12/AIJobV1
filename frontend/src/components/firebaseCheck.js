// // frontend/src/components/FirebaseCheck.js
// import React, { useState } from "react";
// // import { auth } from "../firebase/firebase";
// import { auth } from "../Firebase/firebase";
// import { onAuthStateChanged } from "firebase/auth";

// const FirebaseCheck = () => {
//   const [userInfo, setUserInfo] = useState(null);
//   const [status, setStatus] = useState("Click to check Firebase");

//   const checkFirebase = () => {
//     setStatus("Checking...");
//     onAuthStateChanged(auth, (user) => {
//       if (user) {
//         setUserInfo(user);
//         setStatus("Firebase is working! ✅");
//       } else {
//         setUserInfo(null);
//         setStatus("No user logged in ❌");
//       }
//     });
//   };

//   return (
//     <div>
//       <h2>Firebase Connection Test</h2>
//       <button onClick={checkFirebase}>Check Firebase Auth</button>
//       <p>{status}</p>
//       {userInfo && (
//         <div>
//           <p>Email: {userInfo.email}</p>
//           <p>UID: {userInfo.uid}</p>
//         </div>
//       )}
//     </div>
//   );
// };

// // export default FirebaseCheck;

// // import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

// // const auth = getAuth();

// // signInWithEmailAndPassword(auth, "test@example.com", "yourpassword")
// //   .then((userCredential) => {
// //     userCredential.user.getIdToken().then((idToken) => {
// //       // Send token to backend
// //       fetch("http://127.0.0.1:8000/api/verify-token/", {
// //         method: "GET",
// //         headers: {
// //           Authorization: `Bearer ${idToken}`,
// //         },
// //       })
// //         .then((res) => res.json())
// //         .then((data) => console.log(data))
// //         .catch((err) => console.error(err));
// //     });
// //   })
// //   .catch((error) => {
// //     console.error("Login error:", error);
// //   });

import React, { useState } from "react";
import { auth } from "../Firebase/firebase";
import { 
  onAuthStateChanged,
  createUserWithEmailAndPassword
} from "firebase/auth";

const FirebaseCheck = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [status, setStatus] = useState("Click to check Firebase");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [signUpStatus, setSignUpStatus] = useState("");

  const checkFirebase = () => {
    setStatus("Checking...");
    onAuthStateChanged(auth, (user) => {
      if (user) {
        setUserInfo(user);
        setStatus("Firebase is working! ✅");
      } else {
        setUserInfo(null);
        setStatus("No user logged in ❌");
      }
    });
  };

  const handleSignUp = () => {
    setSignUpStatus("Signing up...");
    createUserWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        setUserInfo(userCredential.user);
        setSignUpStatus("User signed up successfully! ✅");
      })
      .catch((error) => {
        setSignUpStatus(`Error: ${error.message}`);
      });
  };

  return (
    <div>
      <h2>Firebase Connection Test</h2>
      <button onClick={checkFirebase}>Check Firebase Auth</button>
      <p>{status}</p>
      
      {userInfo && (
        <div>
          <p>Email: {userInfo.email}</p>
          <p>UID: {userInfo.uid}</p>
        </div>
      )}

      <hr />

      <h3>Sign Up New User</h3>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      /><br/>
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      /><br/>
      <button onClick={handleSignUp}>Sign Up</button>
      <p>{signUpStatus}</p>
    </div>
  );
};

export default FirebaseCheck;
