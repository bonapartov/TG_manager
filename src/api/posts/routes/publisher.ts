export default {
  routes: [
    {
      method: 'POST',
      path: '/posts/:id/publish-now',
      handler: 'publisher.publishNow',
      config: {
        policies: [],
        middlewares: [],
      },
    },
    {
      method: 'POST',
      path: '/posts/:id/cancel',
      handler: 'publisher.cancel',
      config: {
        policies: [],
        middlewares: [],
      },
    },
    {
      method: 'POST',
      path: '/posts/:id/retry',
      handler: 'publisher.retry',
      config: {
        policies: [],
        middlewares: [],
      },
    },
  ],
};
