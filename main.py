import logging
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes


from Galicia.get_data import get_data, filter_dataframe_based_on_selections, get_dias_aplicacion, categories_to_value_map

TELEGRAM_TOKEN = "7183803554:AAHKiNMonbeVTXYK68TLtTA43JzZB_byn_Y"

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

CHOOSING, RECEIVING_INPUT = range(2)
categories_menu = '''
    *Elige una Categoría:*
    1. 🩻 Salud y Bienestar
    2. 🌭 Gastronomía
    3. 🎬 Entretenimiento
    4. 🛒 Supermercados
    5. 🏠 Hogar
    6. 🛩️ Viajes
    7. 👖 Indumentaria
    8. 👨‍🏫 Educación
    9. 📚 Librerías
    10. 🧸 Juguetes
    11. 🚙 Vehículos
    12. 🖥️ Electrónica
'''

# Define a global DataFrame to store data
data_frame = get_data()

async def start(update: Update, context: CallbackContext):
    mensaje_bienvenida = '''
Hola, soy Savy! Soy un bot que te ayudará a encontrar descuentos de Galicia. \n
*Instrucciones:*
 - Usa /formulario para completar tus datos.
'''

    await update.message.reply_text(mensaje_bienvenida, parse_mode='Markdown')


# Function to download data into the DataFrame
async def choose_card(update: Update, context: CallbackContext) -> None:
    # Inline keyboard setup
    keyboard = [
        [InlineKeyboardButton("Visa Crédito", callback_data='visa_credito'),
         InlineKeyboardButton("MasterCard Crédito", callback_data='master_credito')],
        [InlineKeyboardButton("American Express Crédito", callback_data='amex_credito'),
         InlineKeyboardButton("Galicia Débito", callback_data='debito')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Marca todas las tarjetas que tengas del Banco Galicia. Al finalizar presiona Continuar:', reply_markup=reply_markup)

# Function to update and display the selection keyboard
async def select_cards(update: Update, context: CallbackContext, selected_options_cards=None):
    if selected_options_cards is None:
        selected_options_cards = context.user_data.get('selected_options_cards', set())
    
    # Define buttons with checkmarks for selected options
    keyboard = [
        [InlineKeyboardButton(f"{'✅' if 'visa_credito' in selected_options_cards else ''} Visa Crédito", callback_data='visa_credito'),
         InlineKeyboardButton(f"{'✅' if 'master_credito' in selected_options_cards else ''} MasterCard Crédito", callback_data='master_credito')],
        [InlineKeyboardButton(f"{'✅' if 'amex_credito' in selected_options_cards else ''} American Express Crédito", callback_data='amex_credito'),
         InlineKeyboardButton(f"{'✅' if 'debito' in selected_options_cards else ''} Galicia Débito", callback_data='debito')],
        [InlineKeyboardButton("Continuar", callback_data='submit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Check if it's an update or initial message
    if update.callback_query:
        await update.callback_query.edit_message_text('Al finalizar presiona Continuar:', reply_markup=reply_markup)
    else:
        await update.message.reply_text('Al finalizar presiona Continuar:', reply_markup=reply_markup)


async def choose_category(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user to choose an option."""
    await update.message.reply_text(categories_menu, parse_mode='Markdown')
    return CHOOSING

async def receive_category(update: Update, context: CallbackContext) -> int:
    """Receives the user's choice and checks if it's an integer."""
    user_input = update.message.text
    if user_input.isdigit():
        context.user_data['selected_category'] = int(user_input)  # Store the choice
        await update.message.reply_text(f"Seleccionaste la Categoría: {categories_to_value_map[int(user_input)]}")
        await update.message.reply_text(f"Para ver los descuentos disponibles en esta categoría, usa el comando /show_discounts")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Por favor ingresá un número válido")
        return CHOOSING


# Handling Button Presses for Inline Keyboard (Placeholder, adjust as needed)
async def button(update: Update, context: CallbackContext) -> None:
    global data_frame

    query = update.callback_query
    await query.answer()
    
    # Retrieve stored selections
    selected_options_cards = context.user_data.get('selected_options_cards', set())
    
    # Check which button was pressed
    if query.data == 'submit':
        # Process the final selection
        selected_text = ', '.join(selected_options_cards) if selected_options_cards else 'No options'
    
        await query.edit_message_text(text=f"Elegiste las opciones: {selected_text}")

        #await context.bot.send_message(chat_id=query.message.chat_id, text=f"Selected options: {selected_text}", parse_mode='Markdown')
        await query.message.reply_text(text='Ahora usa el comando /categorias para elegir que tipo de descuentos querés ver.')

    else:
        # Add or remove the selected option
        if query.data in selected_options_cards:
            selected_options_cards.remove(query.data)
        else:
            selected_options_cards.add(query.data)
        context.user_data['selected_options_cards'] = selected_options_cards
        
        # Update the message with new selections
        await select_cards(update, context, selected_options_cards)

async def show_final_data_batches(update: Update, context: CallbackContext) -> None:
    selected_options_cards = context.user_data.get('selected_options_cards', set())
    selected_category = context.user_data.get('selected_category')
    # Filter the DataFrame and keep only the desired columns
    promotions = await filter_dataframe_based_on_selections(data_frame, selected_options_cards, selected_category)

    # Store messages in context to keep track across function calls
    context.user_data['promotions'] = promotions
    context.user_data['next_promotion_index'] = 3 

    await build_and_send_3_promotions(context=context, promotions=promotions[:3], chat_id=update.message.chat_id)
    
    if len(promotions) > 3:
        keyboard = [[InlineKeyboardButton("Ver 3 más", callback_data='show_more_promotions')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Más promociones disponibles:', reply_markup=reply_markup)

async def build_and_send_3_promotions(context, promotions, chat_id):
    for data in promotions:
        data = data['data']
        marca = data['marca']['nombre']
        marca_url = marca.replace(' ', '%20').lower()
        tipo = data['marca']['tipoPromocion'].lower()
        promotion_id = data['id']
        imagen = data['marca']['imagen']
        image_url = f'https://www.galicia.ar/content/dam/galicia/banco-galicia/personas/promociones/catalogo-de-beneficios/{imagen}'
        

        url = f'https://galicia.ar/personas/buscador-de-promociones?path=/promocion/{promotion_id}%7C{marca_url}%7C{tipo}'
        
        text_message = f'''
*Empresa*: {marca}
*Valido*:
- *Desde*: {data['fechaDesde']}
- *Hasta*: {data['fechaHasta']}
*Porcentaje de Ahorro*: {data['porcentajeAhorro']} %
*Cuotas sin Interés*: De {data['cuotaSinInteresDesde']} a {data['cuotaSinInteresHasta']}
*Tope de Reintegro*: ${data['topeReintegro']}
*Días*: {get_dias_aplicacion(data['diasAplicacion'])}
*Solo Eminent*: {'Si' if data['modeloAtencion']['exclusivo'] == True else 'No'}

Click [aquí]({url}) para *más información*.
        '''
        #await update.message.reply_text(text_message)
        await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=text_message, parse_mode='Markdown')

async def show_more_promotions(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    promotions = context.user_data['promotions']
    next_promotion_index = context.user_data['next_promotion_index']
    
    # Calculate the end index for the next batch
    end_index = next_promotion_index + 3
    
    # Send the next batch of messages
    await build_and_send_3_promotions(context=context, promotions=promotions[next_promotion_index:end_index], chat_id=query.message.chat_id)
    
    # Update the index for the next batch
    context.user_data['next_promotion_index'] = end_index
    
    # Edit the current message to remove the "Show 3 more" button or update its text
    if end_index >= len(promotions):
        await query.message.reply_text('No hay más promociones disponibles.')
    else:
        # Only if there are more messages to show
        keyboard = [[InlineKeyboardButton("Ver 3 más", callback_data='show_more_promotions')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text('Más promociones disponibles:', reply_markup=reply_markup)


async def send_image_with_caption(update: Update, context: CallbackContext):
    image_url = 'https://www.galicia.ar/content/dam/galicia/banco-galicia/personas/promociones/catalogo-de-beneficios/toyota_180.png'
    caption = "Here's your image with a caption."
    chat_id = update.message.chat_id
    await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=caption)


async def print_selection(update: Update, context: CallbackContext) -> None:
    """Prints the current selection."""
    choice = context.user_data.get('selected_category')
    if choice is not None:
        await update.message.reply_text(f"Your current selection is: {choice}")
    else:
        await update.message.reply_text("No selection has been made yet.")
    
async def restart_bot(update: Update, context: CallbackContext) -> None:
    # Example of resetting user data
    context.user_data.clear()
    
    # If using a ConversationHandler, you might also end conversations
    # return ConversationHandler.END  # Uncomment if applicable
    
    # Reply to indicate the bot has been "restarted"
    await update.message.reply_text('Savy fue reseteado.')


if __name__ == '__main__':
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('formulario', choose_card))
    application.add_handler(CommandHandler('restart', restart_bot))
    application.add_handler(CommandHandler('show_discounts', show_final_data_batches))
    application.add_handler(CallbackQueryHandler(button, pattern='^(visa_credito|master_credito|amex_credito|debito|submit)$'))
    application.add_handler(CallbackQueryHandler(show_more_promotions, pattern='^show_more_promotions$'))


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('categorias', choose_category)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_category)]
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('print_selection', send_image_with_caption))

    # Start the Bot
    application.run_polling()
