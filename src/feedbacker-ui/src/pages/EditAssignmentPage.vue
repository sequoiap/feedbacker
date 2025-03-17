<template>
  <q-page>
    <!-- <q-input
      v-model="assignment.title"
      class="text-h1"
      filled
    /> -->
    <div class="text-h1" style="cursor: text;" onmouseover="this.style.backgroundColor='#ffe'" onmouseout="this.style.backgroundColor=''">
      {{ assignment.title }}
      <q-popup-edit v-model="assignment.title" auto-save v-slot="scope" @save="updateCellName">
        <q-input v-model="scope.value" label="Edit title" dense autofocus counter @keyup.enter="scope.set" />
      </q-popup-edit>
      <!-- title="Edit title" -->
    </div>
    <!-- <h1>{{ assignment.title }}</h1> -->

    <div class="text-p q-my-md" style="cursor: text;" onmouseover="this.style.backgroundColor='#ffe'" onmouseout="this.style.backgroundColor=''">
      {{ assignment.description }}
      <q-popup-edit v-model="assignment.description" auto-save v-slot="scope" @save="updateCellName">
        <q-input v-model="scope.value" label="Edit description" dense autofocus counter @keyup.enter="scope.set" />
      </q-popup-edit>
      <!-- title="Edit title" -->
    </div>
    <!-- <p>{{ assignment.description }}</p> -->

    <q-list bordered separator>
      <q-item>
        <q-item-section avatar>
          <q-icon name="publish" />
        </q-item-section>
        <q-item-section>Published</q-item-section>
        <q-item-section>
          <q-toggle v-model="published" color="primary" keep-color />
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="calendar_today" />
        </q-item-section>
        <q-item-section>Due date</q-item-section>
        <q-item-section>
          <div>
            <q-input filled v-model="date">
              <template v-slot:prepend>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date v-model="date" mask="YYYY-MM-DD HH:mm">
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Close" color="primary" flat />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>

              <template v-slot:append>
                <q-icon name="access_time" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-time v-model="date" mask="YYYY-MM-DD HH:mm" format24h>
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Close" color="primary" flat />
                      </div>
                    </q-time>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="more_time" />
        </q-item-section>
        <q-item-section>Late submissions</q-item-section>
        <q-item-section>
          <q-select 
            v-model="lateSubmissions" 
            :options="lateOptions" 
            filled
            map-options
          />
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="task_alt" />
        </q-item-section>
        <q-item-section>Attempts allowed</q-item-section>
        <q-item-section>
          <q-input
            v-model.number="attempts"
            type="number"
            filled
          />
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="grading" />
        </q-item-section>
        <q-item-section>Grading policy</q-item-section>
        <q-item-section>
          <q-select 
            v-model="gradingSubmissions" 
            :options="gradingOptions" 
            filled
            map-options
          />
        </q-item-section>
      </q-item>

      <q-item>
        <q-item-section avatar>
          <q-icon name="timer" />
        </q-item-section>
        <q-item-section>Time limit in minutes (0 for unlimited time)</q-item-section>
        <q-item-section>
          <q-input
            v-model.number="timeLimit"
            type="number"
            filled
          />
        </q-item-section>
      </q-item>
    </q-list>

    <div class="q-py-md q-gutter-sm">
      <q-editor 
        v-model="content" 
        min-height="5rem" 
        :toolbar="[
          ['left', 'center', 'right', 'justify'],
          ['bold', 'italic', 'underline', 'strike'],
          ['link', 'image'],
          [
            {
              label: $q.lang.editor.formatting,
              icon: $q.iconSet.editor.formatting,
              list: 'no-icons',
              options: [
                'p',
                'h1',
                'h2',
                'h3',
                'h4',
                'h5',
                'h6',
                'code'
              ]
            },
            {
              label: $q.lang.editor.fontSize,
              icon: $q.iconSet.editor.fontSize,
              fixedLabel: true,
              fixedIcon: true,
              list: 'no-icons',
              options: [
                'size-1',
                'size-2',
                'size-3',
                'size-4',
                'size-5',
                'size-6',
                'size-7'
              ]
            },
            // {
            //   label: $q.lang.editor.defaultFont,
            //   icon: $q.iconSet.editor.font,
            //   fixedIcon: true,
            //   list: 'no-icons',
            //   options: [
            //     'default_font',
            //     'arial',
            //     'arial_black',
            //     'comic_sans',
            //     'courier_new',
            //     'impact',
            //     'lucida_grande',
            //     'times_new_roman',
            //     'verdana'
            //   ]
            // },
            'removeFormat'
          ],
          ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
          ['hr'],
          ['undo', 'redo'],
          ['viewsource']
        ]"
      />
    </div>

    <div class="q-gutter-sm">
      <q-btn color="primary" icon="save" label="Save" />
      <q-btn color="warning" icon="cancel" label="Cancel" />
      <q-btn color="red" icon="delete" label="Delete" />
    </div>
  </q-page>
</template>

<script setup>
import { api } from 'boot/axios';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const published = ref(false);

const assignment = ref({});
const date = ref('');

const lateOptions = [
  { label: 'Not allowed', value: false },
  { label: 'Allowed', value: true },
];
const lateSubmissions = ref(false);

const attempts = ref(0);

const gradingOptions = [
  { label: 'Best attempt', value: 'highest' },
  { label: 'Most recent attempt', value: 'latest' },
  { label: 'First attempt', value: 'first' },
  { label: 'Average of all attempts', value: 'average' },
];
const gradingSubmissions = ref('highest');

const timeLimit = ref(0);

const content = ref('');

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
