const routes = [
  {
    path: '/',
    component: () => import('pages/WelcomePage.vue'),
    name: 'welcome',
  },
  {
    path: '/vote',
    component: () => import('pages/VotePage.vue'),
    name: 'vote',
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
