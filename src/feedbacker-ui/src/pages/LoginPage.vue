<template>
  <q-page>
    <div class="q-pa-md" style="max-width: 400px; width: 100%;">
      <q-form @submit="login">
        <h1 class="text-h4">Login</h1>

        <q-input square filled v-model="username" label="Username" autofocus autocomplete="username" class="full-width"/>
        <q-input square filled v-model="password" label="Password" :type="isPwd ? 'text' : 'password'" autocomplete="current-password" class="full-width q-mt-md">
          <template v-slot:append>
            <q-icon
              :name="isPwd ? 'visibility' : 'visibility_off'"
              @click="isPwd = !isPwd"
              class="cursor-pointer"
            />
          </template>
        </q-input>
        <p class="text-subtitle1 q-pt-md">Don't have an account? Register.</p>
        <q-btn type="submit" label="Login" color="primary" class="q-mt-md" unelevated :loading="isLoading" />
      </q-form>
    </div>
  </q-page>
</template>

<script setup>
import { useAuthStore } from 'src/stores/auth'
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const authStore = useAuthStore()
const $q = useQuasar()

const username = ref('')
const password = ref('')
const isPwd = ref(false)
const isLoading = ref(false)

const login = async () => {
  isLoading.value = true;
  try {
    await authStore.login(username.value, password.value)
  }
  catch (error) {
    console.error('Error logging in:', error)
    if (error == 401) {
      $q.notify({
        color: 'negative',
        position: 'top-right',
        message: 'Invalid username or password',
        icon: 'report_problem',
        actions: [{ label: 'Dismiss', color: 'white' }]
      })
    }
    else {
      $q.notify({
        color: 'negative',
        position: 'top-right',
        message: 'An error occurred while logging in',
        icon: 'report_problem',
        actions: [{ label: 'Dismiss', color: 'white' }]
      })
    }
  }
  finally {
    isLoading.value = false
  }
}
</script>

<style>
  .important { color: #336699; }
</style>
