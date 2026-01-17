import crypto from 'crypto';

function decrypt(enc: string): string {
  const key = process.env.STRAPI_ENCRYPTION_KEY;
  if (!key || key.length < 32) {
    throw new Error('Missing STRAPI_ENCRYPTION_KEY (>=32 chars)');
  }
  const [ivHex, tagHex, dataHex] = enc.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const tag = Buffer.from(tagHex, 'hex');
  const data = Buffer.from(dataHex, 'hex');
  const decipher = crypto.createDecipheriv('aes-256-gcm', Buffer.from(key.slice(0, 32)), iv);
  decipher.setAuthTag(tag);
  const decrypted = Buffer.concat([decipher.update(data), decipher.final()]);
  return decrypted.toString('utf8');
}

async function sendTelegramMessage(token: string, chatId: string, text: string, options: any) {
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  const body: any = {
    chat_id: chatId,
    text,
    parse_mode: options.parse_mode ?? undefined,
    disable_notification: options.disable_notification ?? false,
    protect_content: options.protect_content ?? false,
    reply_markup: options.reply_markup ?? undefined,
  };
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const json: any = await res.json();
  if (!json?.ok) {
    throw new Error(json?.description || 'Telegram API error');
  }
  return (json?.result?.message_id as number) ?? undefined;
}

async function sendTelegramPhoto(token: string, chatId: string, photoUrl: string, caption?: string, options?: any) {
  const url = `https://api.telegram.org/bot${token}/sendPhoto`;
  const body: any = {
    chat_id: chatId,
    photo: photoUrl,
    caption: caption ?? undefined,
    parse_mode: options?.parse_mode ?? undefined,
    has_spoiler: options?.has_spoiler ?? false,
    disable_notification: options?.disable_notification ?? false,
    protect_content: options?.protect_content ?? false,
    reply_markup: options?.reply_markup ?? undefined,
  };
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const json: any = await res.json();
  if (!json?.ok) throw new Error(json?.description || 'Telegram API error');
  return (json?.result?.message_id as number) ?? undefined;
}

async function sendTelegramVideo(token: string, chatId: string, videoUrl: string, caption?: string, options?: any) {
  const url = `https://api.telegram.org/bot${token}/sendVideo`;
  const body: any = {
    chat_id: chatId,
    video: videoUrl,
    caption: caption ?? undefined,
    parse_mode: options?.parse_mode ?? undefined,
    has_spoiler: options?.has_spoiler ?? false,
    disable_notification: options?.disable_notification ?? false,
    protect_content: options?.protect_content ?? false,
    reply_markup: options?.reply_markup ?? undefined,
  };
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const json: any = await res.json();
  if (!json?.ok) throw new Error(json?.description || 'Telegram API error');
  return (json?.result?.message_id as number) ?? undefined;
}

async function sendTelegramDocument(token: string, chatId: string, docUrl: string, caption?: string, options?: any) {
  const url = `https://api.telegram.org/bot${token}/sendDocument`;
  const body: any = {
    chat_id: chatId,
    document: docUrl,
    caption: caption ?? undefined,
    parse_mode: options?.parse_mode ?? undefined,
    disable_notification: options?.disable_notification ?? false,
    protect_content: options?.protect_content ?? false,
    reply_markup: options?.reply_markup ?? undefined,
  };
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const json: any = await res.json();
  if (!json?.ok) throw new Error(json?.description || 'Telegram API error');
  return (json?.result?.message_id as number) ?? undefined;
}

async function sendTelegramMediaGroup(token: string, chatId: string, items: Array<{ type: string; media: string; caption?: string; parse_mode?: string; has_spoiler?: boolean }>, options?: any) {
  const url = `https://api.telegram.org/bot${token}/sendMediaGroup`;
  const body: any = {
    chat_id: chatId,
    media: items.map((it) => ({
      type: it.type,
      media: it.media,
      caption: it.caption,
      parse_mode: it.parse_mode,
      has_spoiler: it.has_spoiler ?? false,
    })),
    disable_notification: options?.disable_notification ?? false,
    protect_content: options?.protect_content ?? false,
  };
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const json: any = await res.json();
  if (!json?.ok) throw new Error(json?.description || 'Telegram API error');
  const first = Array.isArray(json?.result) ? json.result[0] : undefined;
  return (first?.message_id as number) ?? undefined;
}

function getMediaUrl(item: any): string | undefined {
  if (item.external_url) return item.external_url;
  if (item.file) {
    const file = Array.isArray(item.file) ? item.file[0] : item.file;
    if (!file) return undefined;
    const url = file.url;
    if (url.startsWith('http')) return url;
    const baseUrl = process.env.STRAPI_ADMIN_BACKEND_URL || 'http://localhost:1337';
    return `${baseUrl}${url}`;
  }
  return undefined;
}

function buildInlineKeyboardFromComponent(rows: any[]): any | undefined {
  if (!rows || rows.length === 0) return undefined;
  const keyboard = [];
  for (const rowComp of rows) {
    const row = [];
    if (rowComp.buttons) {
      for (const btn of rowComp.buttons) {
        row.push({ text: btn.text, url: btn.url });
      }
    }
    if (row.length > 0) keyboard.push(row);
  }
  return keyboard.length > 0 ? { inline_keyboard: keyboard } : undefined;
}

export default {
  async publishNow(id: number) {
    const post: any = await strapi.entityService.findOne('api::posts.post', id, {
      populate: ['channel', 'media.file', 'buttons.buttons'],
    });
    if (!post) throw new Error('Post not found');
    if (!post.channel) throw new Error('Post has no channel');
    const channel = post.channel as any;
    const chatId = channel.chat_id;
    if (!chatId) throw new Error('Channel chat_id missing');
    const tokenEnc = channel.bot_token_enc;
    if (!tokenEnc) throw new Error('Channel bot_token missing');
    const token = decrypt(tokenEnc);

    const replyMarkup = buildInlineKeyboardFromComponent(post.buttons);
    let msgId: number | undefined;

    const mediaItems: any[] = [];
    if (post.media) {
      for (const m of post.media) {
        const url = getMediaUrl(m);
        if (url) {
          mediaItems.push({
            type: m.type,
            file_path: url,
            caption: m.caption,
          });
        }
      }
    }

    if (mediaItems.length > 0) {
      const first = mediaItems[0];
      const photovidOnly = mediaItems.every((m) => m.type === 'photo' || m.type === 'video');
      
      if (mediaItems.length > 1 && photovidOnly) {
        const items = mediaItems.map((m) => ({
          type: m.type === 'photo' ? 'photo' : 'video',
          media: m.file_path,
          caption: m.caption,
          parse_mode: post.parse_mode,
          has_spoiler: post.has_spoiler,
        }));
        msgId = await sendTelegramMediaGroup(token, chatId, items, {
          disable_notification: post.disable_notification,
          protect_content: post.protect_content,
        });
      } else {
        if (first.type === 'photo') {
          msgId = await sendTelegramPhoto(token, chatId, first.file_path, first.caption ?? post.content, {
            parse_mode: post.parse_mode,
            has_spoiler: post.has_spoiler,
            disable_notification: post.disable_notification,
            protect_content: post.protect_content,
            reply_markup: replyMarkup,
          });
        } else if (first.type === 'video') {
          msgId = await sendTelegramVideo(token, chatId, first.file_path, first.caption ?? post.content, {
            parse_mode: post.parse_mode,
            has_spoiler: post.has_spoiler,
            disable_notification: post.disable_notification,
            protect_content: post.protect_content,
            reply_markup: replyMarkup,
          });
        } else if (first.type === 'document') {
          msgId = await sendTelegramDocument(token, chatId, first.file_path, first.caption ?? post.content, {
            parse_mode: post.parse_mode,
            disable_notification: post.disable_notification,
            protect_content: post.protect_content,
            reply_markup: replyMarkup,
          });
        } else {
          msgId = await sendTelegramMessage(token, chatId, post.content, {
            parse_mode: post.parse_mode,
            disable_notification: post.disable_notification,
            protect_content: post.protect_content,
            reply_markup: replyMarkup,
          });
        }
      }
    } else {
      msgId = await sendTelegramMessage(token, chatId, post.content, {
        parse_mode: post.parse_mode,
        disable_notification: post.disable_notification,
        protect_content: post.protect_content,
        reply_markup: replyMarkup,
      });
    }

    await strapi.entityService.update('api::posts.post', id, {
      data: {
        status: 'published',
        published_msg_id: msgId,
        error_message: null,
      },
    });
    await strapi.entityService.create('api::audit-log.audit-log', {
      data: {
        action: 'publish',
        object_type: 'post',
        object_id: id,
        details: { message_id: msgId },
      },
    });
    return { success: true, message_id: msgId };
  },

  async cancel(id: number) {
    const post: any = await strapi.entityService.findOne('api::posts.post', id);
    if (!post) throw new Error('Post not found');
    if (post.status !== 'scheduled') throw new Error('Post is not scheduled');
    
    await strapi.entityService.update('api::posts.post', id, {
      data: { status: 'cancelled' }
    });
    
    await strapi.entityService.create('api::audit-log.audit-log', {
      data: {
        action: 'cancel',
        object_type: 'post',
        object_id: id,
        details: { previous_status: post.status },
      },
    });
    return { success: true };
  },

  async retry(id: number) {
    const post: any = await strapi.entityService.findOne('api::posts.post', id);
    if (!post) throw new Error('Post not found');
    if (post.status !== 'error') throw new Error('Post is not in error state');
    
    return this.publishNow(id);
  }
};
