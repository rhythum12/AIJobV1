import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCA4pnQyu_vkJWLDVTDoz6CUTrju7gAsik",
  authDomain: "ai-powered-job-recommend-4250d.firebaseapp.com",
  projectId: "ai-powered-job-recommend-4250d",
  storageBucket: "ai-powered-job-recommend-4250d.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef123456"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
