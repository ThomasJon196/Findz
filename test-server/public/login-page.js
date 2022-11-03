"use strict"; // .js strict mode


// Import the functions you need from the SDKs you need
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.13.0/firebase-app.js";


// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCABKarCmyoTQLdXgCq6giVRPj1yC5zPTA",
  authDomain: "findz-e2238.firebaseapp.com",
  projectId: "findz-e2238",
  storageBucket: "findz-e2238.appspot.com",
  messagingSenderId: "125990387562",
  appId: "1:125990387562:web:85882d58c7219805a1af13",
  measurementId: "G-FE8J7NZFT6"
};

// Initialize Firebase
initializeApp(firebaseConfig);

//
// Authentication functions
//
import { GoogleAuthProvider,
         signInWithPopup,
         signOut,
         getAuth,
         createUserWithEmailAndPassword,
         signInWithEmailAndPassword,
         onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.13.0/firebase-auth.js";


async function signIn() {
    // Sign in Firebase using popup auth and Google as the identity provider.
    var provider = new GoogleAuthProvider();
    console.log('Signing in...')
    await signInWithPopup(getAuth(), provider);
    console.log('Signing in complete')

    updateUserTable()
    // const auth = getAuth();
    // var currentUser = auth.currentUser.displayName;
}


function signOutUser() {
    // Sign out of Firebase.
    const auth = getAuth();
    signOut(auth).then(() => {
        console.log('Signed out user.')
    }).catch((error) => {
        console.log('Signed out failed.')
    });
}

// Initialize firebase auth
function initFirebaseAuth() {
    // Listen to auth state changes.
    onAuthStateChanged(getAuth(), authStateObserver);
}

// Returns the signed-in user's profile Pic URL.
function getProfilePicUrl() {
    return getAuth().currentUser.photoURL || '/images/profile_placeholder.png';
}

// Returns the signed-in user's display name.
function getUserName() {
    return getAuth().currentUser.displayName;
}

// Returns the signed-in user's display name.
function getUserMail() {
    return getAuth().currentUser.email;
}

// Returns true if a user is signed-in.
function isUserSignedIn() {
    return !!getAuth().currentUser;
}

// Trigger signIn() on button click
const loginButton = document.getElementById("sign-in");
const logoutButton = document.getElementById("sign-out");

loginButton.addEventListener('click', signIn);
logoutButton.addEventListener('click', signOutUser);


//
// Firestore functions (Database)
//
import { getFirestore, collection, query, where, getDocs, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/9.13.0/firebase-firestore.js";


// Saves a new user to Cloud Firestore.
async function updateUserTable() {
    // Add a new message entry to the Firebase database.


    if (await userExists()){
        console.log('user allready exsits.')
    } else {
        try {
            await addDoc(collection(getFirestore(), 'users'), {
                name: getUserName(),
                email: getUserMail(),
                timestamp: serverTimestamp()
            });
            console.log('Created new user entry.')
        }
        catch (error) {
            console.error('Error writing new user to Firebase Database', error);
        }
    }
}

async function userExists() {
    const email = getUserMail();
    const userRef = collection(getFirestore(), 'users');
    const userQuery = query(userRef, where("email", "==", email))
    const docSnap = await getDocs(userQuery);
    console.log("Executed userExists() query")
    return !(docSnap.empty)
}

async function getUserQuery() {
    const email = getUserMail();
    const userRef = collection(getFirestore(), 'users')
    const userQuery = query(userRef, where("email", "==", email))
    
    const querySnapshot = await getDocs(userQuery);
    querySnapshot.forEach((doc) => {
        // doc.data() is never undefined for query doc snapshots
        console.log(doc.id, " => ", doc.data());
    });
    
    return userQuery
}



//
// Dev-section
//
const debugButton = document.getElementById("debug-information"); // TODO: DELETE
debugButton.addEventListener('click', printDebugInformation)

function printDebugInformation() {
    console.log('User authenticated: ' + !!(getAuth().currentUser))
}

// Could be used for the creation of a new user independend of google.

// createUserWithEmailAndPassword(auth, email, password)
//   .then((userCredential) => {
//     // Signed in 
//     const user = userCredential.user;
//     // ...
//   })
//   .catch((error) => {
//     const errorCode = error.code;
//     const errorMessage = error.message;
//     // ..
//   });


// signInWithEmailAndPassword(auth, email, password)
// .then((userCredential) => {
//     // Signed in 
//     const user = userCredential.user;
//     // ...
// })
// .catch((error) => {
//     const errorCode = error.code;
//     const errorMessage = error.message;
// });

// onAuthStateChanged(auth, (user) => {
//     if (user) {
//       // User is signed in, see docs for a list of available properties
//       // https://firebase.google.com/docs/reference/js/firebase.User
//       const uid = user.uid;
//       // ...
//     } else {
//       // User is signed out
//       // ...
//     }
//   });
// Created based on https://medium.com/swlh/how-to-create-your-first-login-page-with-html-css-and-javascript-602dd71144f1
