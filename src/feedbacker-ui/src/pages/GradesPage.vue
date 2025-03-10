<template>
  <q-page>
    <h1>Grades</h1>

    <div class="q-pa-md">
      <q-table
        title="Grades"
        :rows="grades"
        :columns="columns"
        row-key="name"
      />
    </div>
  </q-page>
</template>

<script setup>
import { inject, onMounted } from 'vue'

const updateDrawer = inject('updateDrawer');

onMounted(() => {
  updateDrawer([
    {
      title: 'View Report',
      caption: 'View it. Do it.',
      icon: 'school',
      link: '/grades/report'
    },
    {
      title: 'Download CSV',
      caption: 'github.com/quasarframework',
      icon: 'code',
      link: '/grades/download'
    },
  ]);
});

const columns = [
  {
    name: 'name',
    required: true,
    label: 'Assignment',
    align: 'left',
    field: row => row.assignment,
    format: val => `${val}`,
    sortable: true
  },
  {
    name: 'score',
    required: false,
    label: 'Score',
    align: 'left',
    field: row => row.score,
    format: val => `${val}`,
    sortable: true
  },
  {
    name: 'possible',
    required: true,
    label: 'Possible',
    align: 'left',
    field: row => row.possible,
    format: val => `${val}`,
    sortable: true
  },
  {
    name: 'percent',
    required: false,
    label: 'Percentage',
    align: 'left',
    field: row => row.score / row.possible * 100,
    format: val => `${val}%`,
    sortable: true
  },
  {
    name: 'attempts',
    required: false,
    label: 'Attempts',
    align: 'left',
    field: row => row.attempts,
    format: val => `${val}`,
    sortable: true
  }
  // { name: 'calcium', label: 'Calcium (%)', field: 'calcium', sortable: true, sort: (a, b) => parseInt(a, 10) - parseInt(b, 10) },
  // { name: 'iron', label: 'Iron (%)', field: 'iron', sortable: true, sort: (a, b) => parseInt(a, 10) - parseInt(b, 10) }
]

let grades = [
  {
    assignment: "Homework 1",
    score: 10,
    possible: 10,
    attempts: 3,
  },
  {
    assignment: "Homework 2",
    score: 8,
    possible: 10,
    attempts: 3,
  },
  {
    assignment: "Homework 3",
    score: null,
    possible: 10,
    attempts: 0,
  },
]
</script>

<style>
  .important { color: #336699; }
</style>
