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
    name: 'home',
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },

  {
    path: '/course',
    component: () => import('layouts/CourseLayout.vue'),
    children: [
      { 
        path: ':id',
        name: 'course',
        component: () => import('pages/CoursePage.vue'),
      },
      {
        path: ':id/assignments',
        name: 'assignments',
        component: () => import('pages/AssignmentsPage.vue')
      },
      {
        path: ':id/assignments/:assnId',
        name: 'assignment',
        component: () => import('pages/AssignmentPage.vue')
      },
      {
        path: ':id/grades',
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
