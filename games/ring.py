import random
from aiogram.types import Message
from db import DB

async def play_ring(msg: Message):
    success = random.choice([True, False])
    result_text = "🏀 Бросок в кольцо...\n"

    if success:
        await DB.execute("UPDATE users SET balance = balance + 50, total_games = total_games + 1, vin_games = vin_games + 1 WHERE telegram_id = $1", msg.from_user.id)
        result_text += "✅ Попадание! +50 к балансу."
    else:
        await DB.execute("UPDATE users SET balance = balance - 10, total_games = total_games + 1 WHERE telegram_id = $1", msg.from_user.id)
        result_text += "❌ Мимо! -10 от баланса."

    return result_text