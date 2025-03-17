<template>
  <q-page>
    <div class="q-gutter-sm">
      <q-btn color="primary" icon="edit" label="Edit" :to="{ name: 'edit_assignment', params: { course_id: $route.params.course_id, assignment_id: $route.params.assignment_id } }" />
      <q-btn color="secondary" icon="send" label="Publish" />
      <q-btn color="red" icon="delete" label="Delete" />
    </div>

    <h1>{{ assignment.title }}</h1>

    <p>{{ assignment.description }}</p>

    <q-list bordered separator>
      <q-item>
        <q-item-section avatar>
          <q-icon name="calendar_today" />
        </q-item-section>
        <q-item-section>Due date</q-item-section>
        <q-item-section>
          {{ DateTime.fromISO(assignment.due_date, { zone: 'utc' }).toLocal().toLocaleString(DateTime.DATETIME_FULL) }} ({{ DateTime.fromISO(assignment.due_date, { zone: 'utc' }).toRelative() }})
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="more_time" />
        </q-item-section>
        <q-item-section>Late submissions</q-item-section>
        <q-item-section>{{ assignment.allow_late_submissions ? 'Allowed' : 'Not allowed' }}</q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="task_alt" />
        </q-item-section>
        <q-item-section>Attempts allowed</q-item-section>
        <q-item-section>{{ assignment.submission_limit > 0 ? assignment.submission_limit : 'No limit' }}</q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="grading" />
        </q-item-section>
        <q-item-section>Grading policy</q-item-section>
        <q-item-section>{{ assignment.grading_policy }}</q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="timer" />
        </q-item-section>
        <q-item-section>Time limit</q-item-section>
        <q-item-section>{{ assignment.time_limit > 0 ? `${assignment.time_limit} minutes` : 'Unlimited time' }}</q-item-section>
      </q-item>
    </q-list>

    <div class="q-py-md">
    {{ assignment.content }}
    </div>

    <q-btn
      color="primary"
      label="Begin attempt"
    />
  </q-page>
</template>

<script setup>
import { api } from 'boot/axios';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { DateTime } from 'luxon';

const route = useRoute();

const assignment = ref({});

const getAssignment = async () => {
  console.log(route.params.assignment_id)
  const response = await api.get(`/assignments/${route.params.assignment_id}`);
  assignment.value = response.data;
  console.log(response.data)
}

onMounted(() => {
  getAssignment();
})
</script>

<style>
  .important { color: #336699; }
</style>
