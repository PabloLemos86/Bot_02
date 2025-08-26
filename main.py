# main.py (modo local / polling com logs e tratamento de erro)

import os
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram import Update
from config import TOKEN
from handlers import registrar_handlers

# ---------- util ----------
def _mask(t: str | None) -> str:
    if not t:
        return "None"
    return f"***{t[-6:]}"

# ---------- validações básicas ----------
if not TOKEN or len(TOKEN.strip()) < 30:
    raise RuntimeError(
        "TOKEN ausente ou inválido. "
        "Defina em config.py (local/PyDroid)."
    )

print(f"[BOOT] Iniciando bot em modo POLLING | TOKEN={_mask(TOKEN)}")

# ---------- instancia o bot ----------
application = ApplicationBuilder().token(TOKEN.strip()).build()

print("[BOOT] Registrando handlers…")
registrar_handlers(application)
print("[BOOT] Handlers registrados com sucesso!")

# ---------- handler global de erros ----------
async def erro_global(update: Update | None, context: ContextTypes.DEFAULT_TYPE):
    if update and update.effective_user:
        user = update.effective_user.username or update.effective_user.id
        print(f"[ERRO] Usuário {user} causou erro: {context.error}")
    else:
        print(f"[ERRO] Um erro ocorreu: {context.error}")

application.add_error_handler(erro_global)

# ---------- execução em polling ----------
if __name__ == "__main__":
    print("[BOOT] Iniciando o bot (modo POLLING)…")
    try:
        application.run_polling()
    except KeyboardInterrupt:
        print("[BOOT] Bot interrompido manualmente.")
    except Exception as e:
        print(f"[ERRO] Falha crítica ao iniciar o bot: {e}")