const routes = [
  // {
  //   path: '/',
  //   component: () => import('layouts/MainLayout.vue'),
  //   children: [
  //     { path: '', component: () => import('pages/IndexPage.vue') }
  //   ]
  // },
  {
    path: '/', redirect: '/courses'
  },

  {
    path: '/login',
    component: () => import('layouts/IndexLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LoginPage.vue') }
    ]
  },

  {
    path: '/courses',
    component: () => import('layouts/MainLayout.vue'),
    name: '',
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') }
    ]
  },

  {
    path: '/course',
    component: () => import('layouts/CourseLayout.vue'),
    children: [
      { 
        path: ':course_id',
        name: 'course',
        component: () => import('pages/CoursePage.vue'),
      },
      {
        path: ':course_id/assignments',
        name: 'assignments',
        component: () => import('pages/AssignmentsPage.vue')
      },
      {
        path: ':course_id/assignments/:assignment_id',
        name: 'assignment',
        component: () => import('pages/AssignmentPage.vue')
      },
      {
        path: ':course_id/assignments/:assignment_id/edit',
        name: 'edit_assignment',
        component: () => import('pages/EditAssignmentPage.vue')
      },
      {
        path: ':course_id/grades',
        name: 'grades',
        component: () => import('pages/GradesPage.vue')
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
