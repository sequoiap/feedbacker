<template>
  <q-page>
    <h1>Assignments</h1>

    <q-list separator>
      <q-item clickable v-for="assn in assignments" :key="assn.code" tag="a" :to="{ name: 'assignment', params: { id: $route.params.id, assnId: assn.code } }">
        <q-item-section>
          <q-item-label>
            {{ assn.name }}
            <q-badge color="primary" label="New" />
          </q-item-label>
          <q-item-label caption>{{ assn.code }}</q-item-label>
        </q-item-section>

        <q-item-section side top>
          <q-item-label caption>{{ assn.instructor }}</q-item-label>
        </q-item-section>
      </q-item>

    </q-list>
  </q-page>
</template>

<script setup>
let assignments = [
  {
    name: "Homework 1",
    code: "ECEN 340",
    instructor: "Steve Schultz",
  },
  {
    name: "Homework 2",
    code: "ECEN 240",
    instructor: "Jeff Goeders",
  },
  {
    name: "Homework 3",
    code: "ECEN 380",
    instructor: "Michael Rice",
  }
]
</script>

<style>
  .important { color: #336699; }
</style>
