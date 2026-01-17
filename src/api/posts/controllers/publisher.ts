export default {
  async publishNow(ctx: any) {
    const id = Number(ctx.params.id);
    if (!id || Number.isNaN(id)) {
      ctx.badRequest('Invalid post id');
      return;
    }
    try {
      const result = await strapi.service('api::posts.publisher').publishNow(id);
      ctx.body = result;
    } catch (e: any) {
      ctx.badRequest(e.message ?? 'Publish failed');
    }
  },

  async cancel(ctx: any) {
    const id = Number(ctx.params.id);
    if (!id || Number.isNaN(id)) {
      ctx.badRequest('Invalid post id');
      return;
    }
    try {
      const result = await strapi.service('api::posts.publisher').cancel(id);
      ctx.body = result;
    } catch (e: any) {
      ctx.badRequest(e.message ?? 'Cancel failed');
    }
  },

  async retry(ctx: any) {
    const id = Number(ctx.params.id);
    if (!id || Number.isNaN(id)) {
      ctx.badRequest('Invalid post id');
      return;
    }
    try {
      const result = await strapi.service('api::posts.publisher').retry(id);
      ctx.body = result;
    } catch (e: any) {
      ctx.badRequest(e.message ?? 'Retry failed');
    }
  },
};
