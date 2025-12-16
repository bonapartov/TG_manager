import asyncio
from typing import Optional, List, Dict, Any
import httpx
from telegram import Bot, InputMediaPhoto, InputMediaVideo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode as TgParseMode
import structlog

from app.core.config import settings
from app.core.security import decrypt_sensitive_data
from app.models.channel import Channel
from app.models.post import Post, PostStatus
from app.schemas.post import MediaItem, ButtonItem

logger = structlog.get_logger(__name__)


class TelegramService:
    """Service for interacting with Telegram API."""
    
    def __init__(self):
        self.bots_cache: Dict[int, Bot] = {}
    
    def get_bot(self, channel: Channel) -> Bot:
        """Get or create bot instance for channel."""
        if channel.id not in self.bots_cache:
            # Decrypt bot token
            bot_token = decrypt_sensitive_data(channel.bot_token_enc)
            self.bots_cache[channel.id] = Bot(token=bot_token)
        
        return self.bots_cache[channel.id]
    
    async def check_channel_access(self, channel: Channel) -> bool:
        """Check if bot has access to channel."""
        try:
            bot = self.get_bot(channel)
            
            # Get chat info
            chat = await bot.get_chat(chat_id=channel.chat_id)
            
            # Get bot member info
            bot_member = await bot.get_chat_member(
                chat_id=channel.chat_id,
                user_id=bot.id
            )
            
            # Check if bot has required permissions
            required_permissions = [
                "can_send_messages",
                "can_send_media_messages",
                "can_send_other_messages"
            ]
            
            for permission in required_permissions:
                if not getattr(bot_member, permission, False):
                    logger.warning(
                        "Bot missing permission",
                        channel_id=channel.id,
                        permission=permission
                    )
                    return False
            
            logger.info(
                "Channel access check passed",
                channel_id=channel.id,
                channel_title=chat.title
            )
            return True
            
        except Exception as e:
            logger.error(
                "Channel access check failed",
                channel_id=channel.id,
                error=str(e)
            )
            return False
    
    async def send_message(
        self,
        channel: Channel,
        text: str,
        parse_mode: str = "Markdown",
        buttons: Optional[List[List[ButtonItem]]] = None,
        disable_notification: bool = False,
        protect_content: bool = False,
        reply_to_message_id: Optional[int] = None
    ) -> int:
        """Send message to channel."""
        try:
            bot = self.get_bot(channel)
            
            # Convert parse mode
            tg_parse_mode = TgParseMode.MARKDOWN if parse_mode == "Markdown" else TgParseMode.HTML
            
            # Convert buttons
            reply_markup = None
            if buttons:
                keyboard = []
                for row in buttons:
                    keyboard_row = []
                    for button in row:
                        keyboard_row.append(
                            InlineKeyboardButton(text=button.text, url=button.url)
                        )
                    keyboard.append(keyboard_row)
                reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send message
            message = await bot.send_message(
                chat_id=channel.chat_id,
                text=text,
                parse_mode=tg_parse_mode,
                reply_markup=reply_markup,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id
            )
            
            logger.info(
                "Message sent successfully",
                channel_id=channel.id,
                message_id=message.message_id
            )
            
            return message.message_id
            
        except Exception as e:
            logger.error(
                "Failed to send message",
                channel_id=channel.id,
                error=str(e)
            )
            raise
    
    async def send_media_group(
        self,
        channel: Channel,
        media: List[MediaItem],
        caption: Optional[str] = None,
        parse_mode: str = "Markdown",
        disable_notification: bool = False,
        protect_content: bool = False
    ) -> List[int]:
        """Send media group to channel."""
        try:
            bot = self.get_bot(channel)
            
            # Convert parse mode
            tg_parse_mode = TgParseMode.MARKDOWN if parse_mode == "Markdown" else TgParseMode.HTML
            
            # Build media group
            media_group = []
            for i, media_item in enumerate(media):
                if media_item.type == "photo":
                    input_media = InputMediaPhoto(
                        media=media_item.file_path,
                        caption=caption if i == 0 else None,
                        parse_mode=tg_parse_mode if i == 0 else None
                    )
                elif media_item.type == "video":
                    input_media = InputMediaVideo(
                        media=media_item.file_path,
                        caption=caption if i == 0 else None,
                        parse_mode=tg_parse_mode if i == 0 else None
                    )
                else:
                    raise ValueError(f"Unsupported media type: {media_item.type}")
                
                media_group.append(input_media)
            
            # Send media group
            messages = await bot.send_media_group(
                chat_id=channel.chat_id,
                media=media_group,
                disable_notification=disable_notification,
                protect_content=protect_content
            )
            
            message_ids = [msg.message_id for msg in messages]
            
            logger.info(
                "Media group sent successfully",
                channel_id=channel.id,
                message_ids=message_ids
            )
            
            return message_ids
            
        except Exception as e:
            logger.error(
                "Failed to send media group",
                channel_id=channel.id,
                error=str(e)
            )
            raise
    
    async def edit_message(
        self,
        channel: Channel,
        message_id: int,
        text: str,
        parse_mode: str = "Markdown",
        buttons: Optional[List[List[ButtonItem]]] = None
    ) -> bool:
        """Edit existing message."""
        try:
            bot = self.get_bot(channel)
            
            # Convert parse mode
            tg_parse_mode = TgParseMode.MARKDOWN if parse_mode == "Markdown" else TgParseMode.HTML
            
            # Convert buttons
            reply_markup = None
            if buttons:
                keyboard = []
                for row in buttons:
                    keyboard_row = []
                    for button in row:
                        keyboard_row.append(
                            InlineKeyboardButton(text=button.text, url=button.url)
                        )
                    keyboard.append(keyboard_row)
                reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Edit message
            await bot.edit_message_text(
                chat_id=channel.chat_id,
                message_id=message_id,
                text=text,
                parse_mode=tg_parse_mode,
                reply_markup=reply_markup
            )
            
            logger.info(
                "Message edited successfully",
                channel_id=channel.id,
                message_id=message_id
            )
            
            return True
            
        except Exception as e:
            logger.error(
                "Failed to edit message",
                channel_id=channel.id,
                message_id=message_id,
                error=str(e)
            )
            return False
    
    async def delete_message(
        self,
        channel: Channel,
        message_id: int
    ) -> bool:
        """Delete message."""
        try:
            bot = self.get_bot(channel)
            
            await bot.delete_message(
                chat_id=channel.chat_id,
                message_id=message_id
            )
            
            logger.info(
                "Message deleted successfully",
                channel_id=channel.id,
                message_id=message_id
            )
            
            return True
            
        except Exception as e:
            logger.error(
                "Failed to delete message",
                channel_id=channel.id,
                message_id=message_id,
                error=str(e)
            )
            return False
    
    async def publish_post(self, post: Post, channel: Channel) -> bool:
        """Publish post to channel."""
        try:
            message_ids = []
            
            # Send media group if there are media files
            if post.media and len(post.media) > 1:
                media_message_ids = await self.send_media_group(
                    channel=channel,
                    media=post.media,
                    caption=post.content,
                    parse_mode=post.parse_mode.value,
                    disable_notification=post.disable_notification,
                    protect_content=post.protect_content
                )
                message_ids.extend(media_message_ids)
            
            # Send single message (either text-only or single media)
            else:
                message_text = post.content
                buttons = None
                
                # If single media file, send it separately
                if post.media and len(post.media) == 1:
                    media_item = post.media[0]
                    if media_item.type == "photo":
                        message_id = await self.send_photo(
                            channel=channel,
                            photo=media_item.file_path,
                            caption=post.content,
                            parse_mode=post.parse_mode.value,
                            buttons=post.buttons,
                            disable_notification=post.disable_notification,
                            protect_content=post.protect_content
                        )
                    elif media_item.type == "video":
                        message_id = await self.send_video(
                            channel=channel,
                            video=media_item.file_path,
                            caption=post.content,
                            parse_mode=post.parse_mode.value,
                            buttons=post.buttons,
                            disable_notification=post.disable_notification,
                            protect_content=post.protect_content
                        )
                    else:
                        # Fallback to text message
                        message_id = await self.send_message(
                            channel=channel,
                            text=post.content,
                            parse_mode=post.parse_mode.value,
                            buttons=post.buttons,
                            disable_notification=post.disable_notification,
                            protect_content=post.protect_content
                        )
                    message_ids.append(message_id)
                else:
                    # Text-only message
                    message_id = await self.send_message(
                        channel=channel,
                        text=message_text,
                        parse_mode=post.parse_mode.value,
                        buttons=buttons,
                        disable_notification=post.disable_notification,
                        protect_content=post.protect_content
                    )
                    message_ids.append(message_id)
            
            # Update post with published message ID
            if message_ids:
                post.published_msg_id = message_ids[0]
                post.status = PostStatus.PUBLISHED
                post.published_at = datetime.utcnow()
                
                logger.info(
                    "Post published successfully",
                    post_id=post.id,
                    channel_id=channel.id,
                    message_ids=message_ids
                )
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(
                "Failed to publish post",
                post_id=post.id,
                channel_id=channel.id,
                error=str(e)
            )
            post.error_message = str(e)
            post.status = PostStatus.ERROR
            return False
    
    async def send_photo(
        self,
        channel: Channel,
        photo: str,
        caption: Optional[str] = None,
        parse_mode: str = "Markdown",
        buttons: Optional[List[List[ButtonItem]]] = None,
        disable_notification: bool = False,
        protect_content: bool = False
    ) -> int:
        """Send photo to channel."""
        try:
            bot = self.get_bot(channel)
            
            # Convert parse mode
            tg_parse_mode = TgParseMode.MARKDOWN if parse_mode == "Markdown" else TgParseMode.HTML
            
            # Convert buttons
            reply_markup = None
            if buttons:
                keyboard = []
                for row in buttons:
                    keyboard_row = []
                    for button in row:
                        keyboard_row.append(
                            InlineKeyboardButton(text=button.text, url=button.url)
                        )
                    keyboard.append(keyboard_row)
                reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send photo
            message = await bot.send_photo(
                chat_id=channel.chat_id,
                photo=photo,
                caption=caption,
                parse_mode=tg_parse_mode,
                reply_markup=reply_markup,
                disable_notification=disable_notification,
                protect_content=protect_content
            )
            
            logger.info(
                "Photo sent successfully",
                channel_id=channel.id,
                message_id=message.message_id
            )
            
            return message.message_id
            
        except Exception as e:
            logger.error(
                "Failed to send photo",
                channel_id=channel.id,
                error=str(e)
            )
            raise
    
    async def send_video(
        self,
        channel: Channel,
        video: str,
        caption: Optional[str] = None,
        parse_mode: str = "Markdown",
        buttons: Optional[List[List[ButtonItem]]] = None,
        disable_notification: bool = False,
        protect_content: bool = False
    ) -> int:
        """Send video to channel."""
        try:
            bot = self.get_bot(channel)
            
            # Convert parse mode
            tg_parse_mode = TgParseMode.MARKDOWN if parse_mode == "Markdown" else TgParseMode.HTML
            
            # Convert buttons
            reply_markup = None
            if buttons:
                keyboard = []
                for row in buttons:
                    keyboard_row = []
                    for button in row:
                        keyboard_row.append(
                            InlineKeyboardButton(text=button.text, url=button.url)
                        )
                    keyboard.append(keyboard_row)
                reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send video
            message = await bot.send_video(
                chat_id=channel.chat_id,
                video=video,
                caption=caption,
                parse_mode=tg_parse_mode,
                reply_markup=reply_markup,
                disable_notification=disable_notification,
                protect_content=protect_content
            )
            
            logger.info(
                "Video sent successfully",
                channel_id=channel.id,
                message_id=message.message_id
            )
            
            return message.message_id
            
        except Exception as e:
            logger.error(
                "Failed to send video",
                channel_id=channel.id,
                error=str(e)
            )
            raise


# Create singleton instance
telegram_service = TelegramService()