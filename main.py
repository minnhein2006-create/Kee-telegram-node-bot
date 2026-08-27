import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

def get_reply_markup():
    keyboard = [
        [KeyboardButton("Node1"), KeyboardButton("Node2")],
        [KeyboardButton("Node3"), KeyboardButton("Node4")],
        [KeyboardButton("Node5"), KeyboardButton("Node6")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_reply_markup()
    msg = await update.message.reply_text("Welcome!", reply_markup=reply_markup)
    
    context.user_data['start_msg_id'] = update.message.message_id
    context.user_data['welcome_msg_id'] = msg.message_id
    
    # ၅ မိနစ် (စက္ကန့် ၃၀၀) နေရင် အော်တိုဖျက်ရန်
    context.job_queue.run_once(delete_message_after_delay, 300, data={"chat_id": msg.chat_id, "message_id": msg.message_id})

async def delete_message_after_delay(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    try:
        await context.bot.delete_message(chat_id=job_data["chat_id"], message_id=job_data["message_id"])
    except Exception as e:
        print(f"Auto-delete error: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Node 1, 2, 3, 4 များအတွက်
    if text in ["Node1", "Node2", "Node3", "Node4"]:
        context.user_data['selected_node'] = text
        context.user_data['node_text_msg_id'] = update.message.message_id
        
        CHANNEL_USERNAME = "@koekee011"  
        
        if text == "Node4":
            VIDEO_MESSAGE_ID = 11
        elif text == "Node3":
            VIDEO_MESSAGE_ID = 3
        elif text == "Node2":
            VIDEO_MESSAGE_ID = 2
        else:
            VIDEO_MESSAGE_ID = 5
        
        inline_keyboard = [
            [InlineKeyboardButton("Get it", callback_data='get_link')]
        ]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)
        caption_text = "Check cc / cc ကိုအရင်ကြည့်ပါ"
        
        try:
            sent_msg = await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_USERNAME,
                message_id=VIDEO_MESSAGE_ID,
                caption=caption_text,
                reply_markup=inline_markup
            )
            context.user_data['video_msg_id'] = sent_msg.message_id
            
            context.job_queue.run_once(delete_message_after_delay, 300, data={"chat_id": sent_msg.chat_id, "message_id": sent_msg.message_id})
        except Exception as e:
            print(f"Error: {e}")
            
    # Node 5 နှင့် 6 တို့အတွက် (Empty စာသား + OK ခလုတ်)
    elif text in ["Node5", "Node6"]:
        context.user_data['selected_node'] = text
        context.user_data['node_text_msg_id'] = update.message.message_id
        
        inline_keyboard = [
            [InlineKeyboardButton("OK", callback_data='ok_close')]
        ]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)
        
        try:
            sent_msg = await update.message.reply_text(
                "𝙀𝙢𝙥𝙩𝙮",
                reply_markup=inline_markup
            )
            context.user_data['video_msg_id'] = sent_msg.message_id
            
            context.job_queue.run_once(delete_message_after_delay, 300, data={"chat_id": sent_msg.chat_id, "message_id": sent_msg.message_id})
        except Exception as e:
            print(f"Error: {e}")

    else:
        reply_msg = await update.message.reply_text("Please choose a valid Node from the menu.", reply_markup=get_reply_markup())
        context.job_queue.run_once(delete_message_after_delay, 300, data={"chat_id": reply_msg.chat_id, "message_id": reply_msg.message_id})

# ခလုတ်များ (Get it / OK) ကို နှိပ်လိုက်သောအခါ
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    CHANNEL_USERNAME = "@koekee011"
    
    # Node 1 မှ 4 အတွက် "Get it" ခလုတ်နှိပ်ပါက
    if query.data == 'get_link':
        selected_node = context.user_data.get('selected_node', 'Node1')
        
        if selected_node == "Node4":
            PHOTO_MESSAGE_ID = 12
            alight_link = "https://alightcreative.com/am/share/u/O0ixdzp1jqZRhCb7hBkmsltTSXm1/p/ZBP999WsPq-5216186cc5ce8f9f"
        elif selected_node == "Node3":
            PHOTO_MESSAGE_ID = 10
            alight_link = "https://alightcreative.com/am/share/u/O0ixdzp1jqZRhCb7hBkmsltTSXm1/p/TV63KrP10Q-182e2f81a7e7c4cf"
        elif selected_node == "Node2":
            PHOTO_MESSAGE_ID = 9
            alight_link = "https://alightcreative.com/am/share/u/O0ixdzp1jqZRhCb7hBkmsltTSXm1/p/WpzshcHZk1-9c1c00a2b568672f"
        else:  # Node1
            PHOTO_MESSAGE_ID = 8
            alight_link = "https://alightcreative.com/am/share/u/O0ixdzp1jqZRhCb7hBkmsltTSXm1/p/YnUoSoCbeX-01135043e6833540"
        
        caption_text = f"𝙃𝙚𝙧𝙚 𝙞𝙨 𝙮𝙤𝙪𝙧 𝙥𝙧𝙚𝙨𝙚𝙩 / 𝙛𝙞𝙡𝙚:\n{alight_link}"
        
        try:
            sent_msg = await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=CHANNEL_USERNAME,
                message_id=PHOTO_MESSAGE_ID,
                caption=caption_text,
                reply_markup=get_reply_markup()
            )
            context.job_queue.run_once(delete_message_after_delay, 300, data={"chat_id": sent_msg.chat_id, "message_id": sent_msg.message_id})
        except Exception as e:
            print(f"Copy message error: {e}")

    # မက်ဆေ့ချ်များ အကုန်လုံးကို ပြိုင်တူ (Parallel) ဖျက်ပေးမည့် Helper Function
    async def safe_delete(m_id):
        if m_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=m_id)
            except Exception:
                pass

    msg_ids_to_delete = [
        context.user_data.get('start_msg_id'),
        context.user_data.get('welcome_msg_id'),
        context.user_data.get('node_text_msg_id'),
        context.user_data.get('video_msg_id'),
        query.message.message_id
    ]

    # asyncio.gather ဖြင့် မက်ဆေ့ချ်အားလုံးကို တစ်ပြိုင်နက် ဖျက်ခိုင်း၍ ပိုမို မြန်ဆန် ချောမွေ့စေသည်
    await asyncio.gather(*(safe_delete(m_id) for m_id in msg_ids_to_delete))

if __name__ == '__main__':
    app = (
        ApplicationBuilder()
        .token("8990820398:AAGOE6HvEiVvVxDeNbkwOKGeKLS1yUQez2o")
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .build()
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot is running...")
    app.run_polling()
          
