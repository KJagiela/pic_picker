const routes = [
  {
    path: '/',
    component: () => import('pages/VotePage.vue'),
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
