from telegram import Update
from fpdf import FPDF
from dotenv import load_dotenv
load_dotenv()
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)


import os
TOKEN = os.getenv("BOT_TOKEN")




# Holatlar ketma-ketligi
(MAHSULOT_NOMI, BUYURTMA_RAQAMI, BUYURTMA_SANASI, FIO, VILOYAT, MANZIL, TEL, MUTAXASSIS,
 MAHSULOT_SONI, SUMMA, YETKAZISH_SANASI) = range(11)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("1. Mahsulot nomini kiriting:")
    return MAHSULOT_NOMI

async def mahsulot_nomi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mahsulot_nomi'] = update.message.text
    await update.message.reply_text("2. Buyurtma raqamini kiriting:")
    return BUYURTMA_RAQAMI

async def buyurtma_raqami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['buyurtma_raqami'] = update.message.text
    await update.message.reply_text("3. Buyurtma olingan sanani kiriting (yyyy-mm-dd):")
    return BUYURTMA_SANASI

async def buyurtma_sanasi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['buyurtma_sanasi'] = update.message.text
    await update.message.reply_text("4. Mijoz F.I.O. ni kiriting:")
    return FIO

async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fio'] = update.message.text
    await update.message.reply_text("5. Mijoz viloyatini kiriting:")
    return VILOYAT

async def viloyat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['viloyat'] = update.message.text
    await update.message.reply_text("6. Mijozning to‘liq manzilini kiriting:")
    return MANZIL

async def manzil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['manzil'] = update.message.text
    await update.message.reply_text("7. Mijoz telefon raqamini kiriting:")
    return TEL

async def tel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['tel'] = update.message.text
    await update.message.reply_text("8. Mutaxassis ismini kiriting:")
    return MUTAXASSIS

async def mutaxassis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mutaxassis'] = update.message.text
    await update.message.reply_text("9. Mahsulot sonini kiriting:")
    return MAHSULOT_SONI

async def mahsulot_soni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mahsulot_soni'] = update.message.text
    await update.message.reply_text("10. Mahsulot umumiy summasini kiriting:")
    return SUMMA

async def summa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['summa'] = update.message.text
    await update.message.reply_text("11. Yetkazib berish sanasini kiriting (yyyy-mm-dd):")
    return YETKAZISH_SANASI

async def yetkazish_sanasi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['yetkazish_sanasi'] = update.message.text

    # PDF yaratamiz
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Buyurtma Tafsilotlari", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Mahsulot nomi: {context.user_data['mahsulot_nomi']}", ln=True)
    pdf.cell(200, 10, txt=f"Buyurtma raqami: {context.user_data['buyurtma_raqami']}", ln=True)
    pdf.cell(200, 10, txt=f"Buyurtma sanasi: {context.user_data['buyurtma_sanasi']}", ln=True)
    pdf.cell(200, 10, txt=f"Mijoz F.I.O: {context.user_data['fio']}", ln=True)
    pdf.cell(200, 10, txt=f"Mijoz viloyati: {context.user_data['viloyat']}", ln=True)
    pdf.cell(200, 10, txt=f"Mijoz manzili: {context.user_data['manzil']}", ln=True)
    pdf.cell(200, 10, txt=f"Telefon raqami: {context.user_data['tel']}", ln=True)
    pdf.cell(200, 10, txt=f"Mutaxassis: {context.user_data['mutaxassis']}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="--- BUYURTMA MA'LUMOTI ---", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Mahsulot nomi: {context.user_data['mahsulot_nomi']}", ln=True)
    pdf.cell(200, 10, txt=f"Mahsulot soni: {context.user_data['mahsulot_soni']}", ln=True)
    pdf.cell(200, 10, txt=f"Umumiy summa: {context.user_data['summa']} so'm", ln=True)
    pdf.cell(200, 10, txt=f"Yetkazib berish sanasi: {context.user_data['yetkazish_sanasi']}", ln=True)
    filename = f"buyurtma_{context.user_data['buyurtma_raqami']}.pdf"
    pdf.output(filename)

    # Foydalanuvchiga yuborish
    with open(filename, "rb") as f:
        await update.message.reply_document(document=f, filename=filename)

    os.remove(filename)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Buyurtma jarayoni bekor qilindi.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAHSULOT_NOMI: [MessageHandler(filters.TEXT & ~filters.COMMAND, mahsulot_nomi)],
            BUYURTMA_RAQAMI: [MessageHandler(filters.TEXT & ~filters.COMMAND, buyurtma_raqami)],
            BUYURTMA_SANASI: [MessageHandler(filters.TEXT & ~filters.COMMAND, buyurtma_sanasi)],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, fio)],
            VILOYAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, viloyat)],
            MANZIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, manzil)],
            TEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, tel)],
            MUTAXASSIS: [MessageHandler(filters.TEXT & ~filters.COMMAND, mutaxassis)],
            MAHSULOT_SONI: [MessageHandler(filters.TEXT & ~filters.COMMAND, mahsulot_soni)],
            SUMMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, summa)],
            YETKAZISH_SANASI: [MessageHandler(filters.TEXT & ~filters.COMMAND, yetkazish_sanasi)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == '__main__':
    main()

