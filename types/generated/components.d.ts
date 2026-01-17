import type { Schema, Struct } from '@strapi/strapi';

export interface SharedButtonRow extends Struct.ComponentSchema {
  collectionName: 'components_shared_button_rows';
  info: {
    displayName: 'Button Row';
    icon: 'bars';
  };
  attributes: {
    buttons: Schema.Attribute.Component<'shared.telegram-button', true>;
  };
}

export interface SharedTelegramButton extends Struct.ComponentSchema {
  collectionName: 'components_shared_telegram_buttons';
  info: {
    displayName: 'Telegram Button';
    icon: 'link';
  };
  attributes: {
    text: Schema.Attribute.String & Schema.Attribute.Required;
    url: Schema.Attribute.String & Schema.Attribute.Required;
  };
}

export interface SharedTelegramMedia extends Struct.ComponentSchema {
  collectionName: 'components_shared_telegram_medias';
  info: {
    displayName: 'Telegram Media';
    icon: 'picture';
  };
  attributes: {
    caption: Schema.Attribute.Text;
    external_url: Schema.Attribute.String;
    file: Schema.Attribute.Media<'images' | 'videos' | 'files'>;
    type: Schema.Attribute.Enumeration<['photo', 'video', 'document']> &
      Schema.Attribute.Required &
      Schema.Attribute.DefaultTo<'photo'>;
  };
}

declare module '@strapi/strapi' {
  export module Public {
    export interface ComponentSchemas {
      'shared.button-row': SharedButtonRow;
      'shared.telegram-button': SharedTelegramButton;
      'shared.telegram-media': SharedTelegramMedia;
    }
  }
}
