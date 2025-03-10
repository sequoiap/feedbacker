<template>
  <q-page>
    <h1>Specific Assignment</h1>

    <q-list bordered separator>
      <q-item>
        <q-item-section avatar>
          <q-icon name="task_alt" />
        </q-item-section>
        <q-item-section>Attempts</q-item-section>
        <q-item-section>3</q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="calendar_today" />
        </q-item-section>
        <q-item-section>Due date</q-item-section>
        <q-item-section>May 12, 2025</q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="timer" />
        </q-item-section>
        <q-item-section>Time limit</q-item-section>
        <q-item-section>3 hours</q-item-section>
      </q-item>
    </q-list>

    <div>
    <h2>Homework 1</h2>

    <p>This is the content of the homework assignment.</p>
    
    <h3>Problem 1</h3>

    <p>This is the first problem.</p>
    
    <h3>Problem 2</h3>

    <p>This is the second problem.</p>
    
    <h3>Submission Instructions</h3>

    <p>Upload your netlist file by the due date. Unlimited submissions are allowed.</p>
    </div>

    <q-btn
      color="primary"
      label="Begin attempt"
    />
  </q-page>
</template>

<script setup>
//
</script>

<style>
  .important { color: #336699; }
</style>
