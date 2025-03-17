<template>
  <q-layout view="hHr LpR fFr">
    <q-header elevated>
      <div class="text-white" style="background-color: rgb(50, 93, 136);">
        <q-toolbar>
          <q-icon name="img:icons/check-double_poly.svg" size="2em" />
          <q-toolbar-title>
            Feedbacker
          </q-toolbar-title>

          <q-space />
          
          {{ displayName }}
          <q-btn flat round dense icon="account_circle" />
        </q-toolbar>
      </div>

      <div style="background-color: #f8f5f0;">
        <q-toolbar inset>
        </q-toolbar>
      </div>
    </q-header>

    <q-footer>
      <q-toolbar>
        <div>
          &copy; Copyright 2024 by <a href="https://github.com/sequoiap" style="color: white">Sequoia Ploeg</a>.
          <br>
          <small><em>Cookies must be enabled for this site to work properly.</em></small>
        </div>
      </q-toolbar>
    </q-footer>

    <q-page-container class="q-pa-lg">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore()

const displayName = computed(() => {
  return `${authStore.user?.firstname} ${authStore.user?.lastname}`
})
</script>
