export default {
  /**
   * Placeholder cron task. Later, this will process scheduled posts.
   */
  '*/2 * * * *': async ({ strapi }) => {
    try {
      const now = new Date();
      const due = await strapi.entityService.findMany('api::posts.post', {
        filters: { status: 'scheduled', publish_at: { $lte: now.toISOString() } },
        populate: ['channel'],
        limit: 25,
      });
      for (const post of due as any[]) {
        try {
          await strapi.service('api::posts.publisher').publishNow(post.id);
        } catch (e) {
          await strapi.entityService.update('api::posts.post', post.id, {
            data: { status: 'error', error_message: (e as any)?.message ?? 'Publish error' },
          });
          await strapi.entityService.create('api::audit-log.audit-log', {
            data: {
              action: 'publish',
              object_type: 'post',
              object_id: post.id,
              details: { error: (e as any)?.message },
            },
          });
        }
      }
    } catch (e) {
      // Silent catch
    }
  },
};
