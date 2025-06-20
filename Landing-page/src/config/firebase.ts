import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyC1-m6sbveASRS9U_VUb4LNyGWCocGcUqc",
  authDomain: "axiom-463504.firebaseapp.com",
  projectId: "axiom-463504",
  storageBucket: "axiom-463504.firebasestorage.app",
  messagingSenderId: "844148800303",
  appId: "1:844148800303:web:735145ee63c01b62ffffda",
  measurementId: "G-GQQZQ2JYLN"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// Initialize Analytics
export const analytics = getAnalytics(app);

// Initialize Firestore and export
export const db = getFirestore(app);

export default app;