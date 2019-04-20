// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
  production: false,
  backendHostUrl: "http://localhost:8081",
  firebase: {
    apiKey: "AIzaSyBdTAbnhQ0aEHHNj9Tr1xp3tHjje7ZowM0",
    authDomain: "cuez-fb8d0.firebaseapp.com",
    databaseURL: "https://cuez-fb8d0.firebaseio.com",
    projectId: "cuez-fb8d0",
    storageBucket: "cuez-fb8d0.appspot.com",
    messagingSenderId: "543348701259"
  }
};
