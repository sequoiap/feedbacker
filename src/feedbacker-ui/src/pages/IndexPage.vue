<template>
  <q-page>
    <h1>My Courses</h1>

    <q-list separator>
      <q-item clickable v-for="course in courses" :key="course.code" tag="a" :to="{ name: 'course', params: { id: course.code } }">
        <q-item-section>
          <q-item-label>
            {{ course.name }}
            <q-badge color="primary" label="New" />
          </q-item-label>
          <q-item-label caption>{{ course.code }}</q-item-label>
        </q-item-section>

        <q-item-section side top>
          <q-item-label caption>{{ course.instructor }}</q-item-label>
        </q-item-section>
      </q-item>

    </q-list>
  </q-page>
</template>

<script setup>
let courses = [
  {
    name: "Circuits",
    code: "ECEN 340",
    instructor: "Steve Schultz",
  },
  {
    name: "Digital Systems",
    code: "ECEN 240",
    instructor: "Jeff Goeders",
  },
  {
    name: "Signals and Systems",
    code: "ECEN 380",
    instructor: "Michael Rice",
  }
]
</script>

<style>
  .important { color: #336699; }
</style>
