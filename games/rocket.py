import random
from aiogram.types import Message
from db import DB

async def play_rocket(msg: Message, target_multiplier: float):
    max_multiplier = random.choice([1.1, 1.5, 2, 2.5, 3, 3.5])
    result_text = f"🚀 Ракета стартовала... Цель: x{target_multiplier}\n"

    if max_multiplier >= target_multiplier:
        winnings = int(10 * target_multiplier)
        await DB.execute("UPDATE users SET balance = balance + $1, total_games = total_games + 1, vin_games = vin_games + 1 WHERE telegram_id = $2", winnings, msg.from_user.id)
        result_text += f"✅ Успех! Ракета достигла x{max_multiplier}. Выигрыш: +{winnings}"
    else:
        await DB.execute("UPDATE users SET balance = balance - 10, total_games = total_games + 1 WHERE telegram_id = $1", msg.from_user.id)
        result_text += f"💥 Неудача. Ракета упала на x{max_multiplier}. Потеря: -10"

    return result_text