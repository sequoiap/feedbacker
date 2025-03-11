import { defineStore, acceptHMRUpdate } from 'pinia'
import axios from 'axios';
import { api } from 'boot/axios';
import { ref } from 'vue'
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('authStore', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')));
  const accessToken = ref(localStorage.getItem('access_token'));
  const returnUrl = ref('');
  const router = useRouter();

  const login = async (username, password) => {
    const form_data = new FormData()
    form_data.append("username", username)
    form_data.append("password", password)

    await axios
      .post('/auth/login', form_data)
      .then(response => {
        console.log('auth response', response.data);
        localStorage.setItem('access_token', response.data.access_token);
        accessToken.value = response.data.access_token;
        user.value = response.data;
        router.push(returnUrl.value || '/');
      })
      .catch(error => {
        console.log(error);
        if (error.response.status === 401) {
          console.log('Invalid credentials');
          throw 401;
        }
        else if (error.response.status === 500) {
          console.log('Server error');
          throw 500;
        }
        else {
          console.log('Unknown error');
          throw 0;
        }
      })

    await api
      .get('/auth/me')
      .then(response => {
        console.log('me response', response.data);
        user.value = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
      })
      .catch(error => {
        console.log(error);
        throw 0;
      })
  }

  return { login, accessToken, user }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
}
