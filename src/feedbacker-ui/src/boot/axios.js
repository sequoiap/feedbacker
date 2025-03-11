import { defineBoot } from '#q-app/wrappers'
import axios from 'axios'
import { useAuthStore } from 'src/stores/auth';

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1'

const api = axios.create({
  withCredentials: true,
})

const refresh = axios.create({
  withCredentials: true,
})

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

let isRefreshing = false;
let refreshQueue = [];

api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const authStore = useAuthStore();
    if ((error.response.status === 401) && !error.config._retry) {
      // Try to refresh the token. Only the first request to fail should try
      // to refresh the token, the rest should wait for the first to finish
      if (!isRefreshing) {
        // Set the variable to prevent other requests from refreshing the token
        isRefreshing = true;
        // Try to refresh the token
        try {
          error.config._retry = true;
          await refreshToken();
          return api(error.config);
        } 
        // If the refresh token fails, clear the queue and logout the user
        catch (e) {
          console.log(e);
          refreshQueue = [];
          authStore.logout();
          return Promise.reject(error);
        } 
        // Reset the variable and process the queue
        finally {
          isRefreshing = false;
          refreshQueue.forEach((resolve) => resolve());
          refreshQueue = [];
        }
      } 
      // A request is already attempting to refresh the token, so we queue
      // subsequent requests until the token is refreshed
      else {
        return new Promise((resolve) => {
          refreshQueue.push(() => {
            resolve(api(error.config));
          });
        });
      }
    }
    return Promise.reject(error);
  }
)

const refreshToken = async () => {
  const authStore = useAuthStore();
  try {
    const response = await refresh.post('/auth/refresh');
    authStore.setTokens(response.data.access, response.data.refresh);
    return response;
  } catch (e) {
    return Promise.reject(e);
  }
}

export default defineBoot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { api }
