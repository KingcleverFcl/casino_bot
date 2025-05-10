import random
from aiogram.types import Message
from db import DB

async def play_dice(msg: Message, chosen: int):
    dice_roll = random.randint(1, 6)
    result_text = f"Вы выбрали {chosen} 🎲
Выпало: {dice_roll} 🎲\n"

    if dice_roll == chosen:
        await DB.execute("UPDATE users SET balance = balance + 50, total_games = total_games + 1, vin_games = vin_games + 1 WHERE telegram_id = $1", msg.from_user.id)
        result_text += "✅ Победа! +50 к балансу."
    else:
        await DB.execute("UPDATE users SET balance = balance - 10, total_games = total_games + 1 WHERE telegram_id = $1", msg.from_user.id)
        result_text += "❌ Проигрыш. -10 от баланса."

    return result_text