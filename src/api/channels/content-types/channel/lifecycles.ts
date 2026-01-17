import crypto from 'crypto';

function encrypt(value: string): string {
  const key = process.env.STRAPI_ENCRYPTION_KEY;
  if (!key || key.length < 32) {
    throw new Error('Missing STRAPI_ENCRYPTION_KEY (>=32 chars)');
  }
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', Buffer.from(key.slice(0, 32)), iv);
  const encrypted = Buffer.concat([cipher.update(value, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return `${iv.toString('hex')}:${tag.toString('hex')}:${encrypted.toString('hex')}`;
}

const lifecycles = {
  async beforeCreate(event: any) {
    const data = event.params.data as Record<string, unknown>;
    if (typeof data.bot_token_enc === 'string' && data.bot_token_enc) {
      data.bot_token_enc = encrypt(data.bot_token_enc);
    }
  },
  async beforeUpdate(event: any) {
    const data = event.params.data as Record<string, unknown>;
    if (typeof data.bot_token_enc === 'string' && data.bot_token_enc) {
      // Re-encrypt only if looks like plaintext (no expected separators)
      const token = data.bot_token_enc as string;
      if (!token.includes(':')) {
        data.bot_token_enc = encrypt(token);
      }
    }
  },
};

export default lifecycles;
