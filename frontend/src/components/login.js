import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "./firebase";

signInWithEmailAndPassword(auth, email, password)
  .then(async (userCredential) => {
    const token = await userCredential.user.getIdToken();
    
    // Send token to Django
    await fetch("/api/verify-token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });
  });
