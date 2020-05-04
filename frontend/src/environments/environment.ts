import { AUTH_CONFIG} from '../../auth0-variables';

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: AUTH_CONFIG.url, // the auth0 domain prefix
    audience: AUTH_CONFIG.audience, // the audience set for the auth0 app
    clientId: AUTH_CONFIG.clientId, // the client id generated for the auth0 app
    callbackURL: AUTH_CONFIG.callbackURL, // the base url of the running ionic application.
  }
};
