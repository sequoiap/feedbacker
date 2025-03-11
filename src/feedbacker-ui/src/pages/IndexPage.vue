<template>
  <q-page>
    <h1>My Courses</h1>

    <q-list separator>
      <q-item clickable v-for="course in courses" :key="course.id" tag="a" :to="{ name: 'course', params: { id: course.id } }">
        <q-item-section>
          <q-item-label>
            {{ course.name }}
            <q-badge v-if="iAmInstructor(course.instructors)" color="primary" label="Instructor" />
          </q-item-label>
          <q-item-label caption>{{ course.code }}</q-item-label>
        </q-item-section>

        <q-item-section side top>
          <q-item-label caption>{{ formatInstructorLabel(course.instructors) }}</q-item-label>
        </q-item-section>
      </q-item>

    </q-list>
  </q-page>
</template>

<script setup>
import { api } from 'boot/axios';
import { ref, onMounted } from 'vue';
import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore()

const courses = ref([]);

const getCourses = async () => {
  const response = await api.get('/courses', { params: { user_id: authStore.user.id } });
  courses.value = response.data;
  console.log(response.data)
}

const formatInstructorLabel = (instructors) => {
  return instructors.map(i => `${i.firstname} ${i.lastname}`).join(', ');
}

const iAmInstructor = (instructors) => {
  return instructors.some(i => i.id === authStore.user.id);
}

onMounted(() => {
  getCourses();
})
</script>

<style>
  .important { color: #336699; }
</style>
