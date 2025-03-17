<template>
  <q-page>
    <h1>Assignments</h1>

    <div class="q-gutter-sm">
      <q-btn color="primary" icon="add" label="Create New" />
      <!-- <q-btn color="warning" icon="cancel" label="Cancel" />
      <q-btn color="red" icon="delete" label="Delete" /> -->
    </div>

    <q-list separator class="q-my-md">
      <template v-if="assignments.length === 0">
        <q-item>
          <q-item-section>
            <q-item-label>
              No assignments yet.
            </q-item-label>
          </q-item-section>
        </q-item>
      </template>

      <q-item clickable v-for="assn in assignments" :key="assn.code" tag="a" :to="{ name: 'assignment', params: { course_id: $route.params.course_id, assignment_id: assn.id } }">
        <q-item-section>
          <q-item-label>
            {{ assn.title }}
            <q-badge color="primary" label="New" />
          </q-item-label>
          <q-item-label caption>{{ assn.description }}</q-item-label>
        </q-item-section>

        <q-item-section side top>
          <q-item-label caption>{{ assn.instructor }}</q-item-label>
        </q-item-section>
      </q-item>

    </q-list>
  </q-page>
</template>

<script setup>
import { api } from 'boot/axios';
import { ref, onMounted } from 'vue';
// import { useAuthStore } from 'src/stores/auth';
import { useRoute } from 'vue-router';

// const authStore = useAuthStore()

const route = useRoute();
const assignments = ref([]);

const getAssignments = async () => {
  const response = await api.get('/assignments', { params: { course_id: route.params.course_id } });
  assignments.value = response.data;
  console.log(response.data)
}

onMounted(() => {
  getAssignments();
})
</script>

<style>
  .important { color: #336699; }
</style>
