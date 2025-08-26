# handlers.py
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from config import REGIOES, DEFAULT_QTD
from utils.licitacoes import coletar_licitacoes, enviar_licitacoes

# ========= COMANDOS =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bem-vindo! Use o botão ☰ Menu abaixo para começar.")

async def comando_pesquisar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌎 Norte", callback_data="regiao_Norte")],
        [InlineKeyboardButton("🌎 Nordeste", callback_data="regiao_Nordeste")],
        [InlineKeyboardButton("🌎 Centro-Oeste", callback_data="regiao_Centro-Oeste")],
        [InlineKeyboardButton("🌎 Sudeste", callback_data="regiao_Sudeste")],
        [InlineKeyboardButton("🌎 Sul", callback_data="regiao_Sul")],
        [InlineKeyboardButton("🌎 Nacional", callback_data="regiao_Nacional")],
    ]
    await update.message.reply_text("Selecione a região:", reply_markup=InlineKeyboardMarkup(keyboard))

async def comando_creditos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("20 créditos – R$0,01", callback_data="recarga_20")],
        [InlineKeyboardButton("50 créditos – R$0,02", callback_data="recarga_50")],
        [InlineKeyboardButton("80 créditos – R$0,03", callback_data="recarga_80")],
    ]
    await update.message.reply_text(
        "💳 Seu saldo atual é: 10 créditos.\n\nEscolha uma opção para recarregar:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def comando_agendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Em breve você poderá agendar pesquisas automáticas!")

# ========= CALLBACKS =========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("regiao_"):
        regiao = data.split("_", 1)[1]
        context.user_data["regiao"] = regiao
        estados = REGIOES.get(regiao, [])
        if estados:
            # Grade 3xN de estados
            keyboard = [
                [InlineKeyboardButton(uf, callback_data=f"estado_{uf}") for uf in estados[i:i+3]]
                for i in range(0, len(estados), 3)
            ]
            await query.edit_message_text(
                f"Região *{regiao}* selecionada. Agora escolha o estado:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
        else:
            context.user_data["uf"] = None
            await mostrar_opcoes_periodo(query)
        return

    if data.startswith("estado_"):
        uf = data.split("_", 1)[1]
        context.user_data["uf"] = uf
        await mostrar_opcoes_periodo(query)
        return

    if data.startswith("periodo_"):
        dias = int(data.split("_", 1)[1])
        hoje = datetime.now()
        data_inicial = hoje - timedelta(days=dias)
        data_final = hoje
        uf = context.user_data.get("uf")
        await query.edit_message_text(
            f"🔍 Buscando licitações para `{uf or 'Brasil inteiro'}` de {data_inicial.date()} a {data_final.date()}...",
            parse_mode="Markdown"
        )
        lics = coletar_licitacoes(
            data_inicial.strftime("%Y%m%d"),
            data_final.strftime("%Y%m%d"),
            uf=uf,
            limite=DEFAULT_QTD
        )
        if not lics:
            await query.message.reply_text("⚠️ Nenhuma licitação encontrada.")
            return
        await enviar_licitacoes(query, lics)
        return

    if data.startswith("recarga_"):
        valor = data.split("_", 1)[1]
        creditos_map = {"20": "R$0,01", "50": "R$0,02", "80": "R$0,03"}
        valor_real = creditos_map.get(valor, "valor desconhecido")
        await query.edit_message_text(
            f"✅ Você escolheu recarregar {valor} créditos por {valor_real}.\n\n🔜 Em breve o pagamento será processado!"
        )

# ========= AUXILIARES =========
async def mostrar_opcoes_periodo(query):
    keyboard = [
        [InlineKeyboardButton("🗓️ Últimos 7 dias", callback_data="periodo_7")],
        [InlineKeyboardButton("🗓️ Últimos 15 dias", callback_data="periodo_15")],
        [InlineKeyboardButton("🗓️ 1 mês", callback_data="periodo_30")],
        [InlineKeyboardButton("🗓️ 3 meses", callback_data="periodo_90")],
    ]
    await query.edit_message_text("Agora selecione o período:", reply_markup=InlineKeyboardMarkup(keyboard))

async def configurar_menu(app):
    comandos = [
        BotCommand("start", "Início"),
        BotCommand("pesquisar", "🔍 Pesquisar licitações"),
        BotCommand("agendar", "📅 Agendar busca automática"),
        BotCommand("creditos", "💳 CRÉDITOS"),
    ]
    await app.bot.set_my_commands(comandos)

def registrar_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pesquisar", comando_pesquisar))
    application.add_handler(CommandHandler("creditos", comando_creditos))
    application.add_handler(CommandHandler("agendar", comando_agendar))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.post_init = configurar_menu