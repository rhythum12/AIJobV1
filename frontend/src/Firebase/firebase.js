import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCA4pnQyu_vkJWLDVTDoz6CUTrju7gAsik",
  authDomain: "ai-powered-job-recommend-4250d.firebaseapp.com",
  projectId: "ai-powered-job-recommend-4250d",
  storageBucket: "your-app.appspot.com",
  messagingSenderId: "sender-id",
  appId: "app-id"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
