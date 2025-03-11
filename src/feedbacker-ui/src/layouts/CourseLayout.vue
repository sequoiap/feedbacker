<template>
  <q-layout view="hHr LpR fFr">
    <q-header elevated>
      <div class="text-white" style="background-color: rgb(50, 93, 136);">
        <q-toolbar>

          <!-- <q-btn
            flat
            dense
            round
            icon="menu"
            aria-label="Menu"
            @click="toggleLeftDrawer"
          /> -->
          
          <q-icon name="img:icons/check-double_poly.svg" size="2em" />
          <q-toolbar-title> 
            <router-link class="q-toolbar__title ellipsis" style="text-decoration: none; color: inherit;" to="/">Feedbacker</router-link>
          </q-toolbar-title>
          <!-- <q-toolbar-title>
            Feedbacker
          </q-toolbar-title> -->

          <q-space />

          {{ displayName}}
          <q-btn flat round dense icon="account_circle" />
        </q-toolbar>
      </div>

      <div style="background-color: #f8f5f0;">
        <q-toolbar inset>
          <q-btn square flat color="primary" icon="home" label="Home" :to="{ name: 'course', params: { id: $route.params.id } }" />
          <q-btn square flat color="primary" icon="assignment" label="Assignments" :to="{ name: 'assignments', params: { id: $route.params.id } }" />
          <q-btn square flat color="primary" icon="grading" label="Grades" :to="{ name: 'grades', params: { id: $route.params.id } }" />
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

    
    <q-drawer
      v-model="leftDrawerOpen"
      bordered
      class="bg-grey-3"
    >
      <slot name="drawer-content">
        <q-list>
          <q-item-label
            header
          >
            Essential Links
          </q-item-label>

          <EssentialLink
            v-for="link in drawerItems"
            :key="link.title"
            v-bind="link"
          />
        </q-list>
      </slot>
    </q-drawer>

    <q-page-container class="q-ma-lg">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, provide, computed } from 'vue'
import { useAuthStore } from 'src/stores/auth';
import EssentialLink from 'components/EssentialLink.vue'

const authStore = useAuthStore()

const displayName = computed(() => {
  return `${authStore.user.firstname} ${authStore.user.lastname}`
})

const leftDrawerOpen = ref(true)

const linksList = [
  {
    title: 'Docs',
    caption: 'quasar.dev',
    icon: 'school',
    link: 'https://quasar.dev'
  },
  {
    title: 'Github',
    caption: 'github.com/quasarframework',
    icon: 'code',
    link: 'https://github.com/quasarframework'
  },
  {
    title: 'Discord Chat Channel',
    caption: 'chat.quasar.dev',
    icon: 'chat',
    link: 'https://chat.quasar.dev'
  },
  {
    title: 'Forum',
    caption: 'forum.quasar.dev',
    icon: 'record_voice_over',
    link: 'https://forum.quasar.dev'
  },
  {
    title: 'Twitter',
    caption: '@quasarframework',
    icon: 'rss_feed',
    link: 'https://twitter.quasar.dev'
  },
  {
    title: 'Facebook',
    caption: '@QuasarFramework',
    icon: 'public',
    link: 'https://facebook.quasar.dev'
  },
  {
    title: 'Quasar Awesome',
    caption: 'Community Quasar projects',
    icon: 'favorite',
    link: 'https://awesome.quasar.dev'
  }
]

const drawerItems = ref(linksList);

const updateDrawer = (items) => {
  drawerItems.value = items;
};

provide('updateDrawer', updateDrawer);
</script>
