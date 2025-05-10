import random
from db import DB

def generate_field():
    cells = ["⭐"] * 15 + ["💣"] * 10
    random.shuffle(cells)
    return [cells[i:i+5] for i in range(0, 25, 5)]

def display_field(field, revealed):
    display = ""
    for i in range(5):
        for j in range(5):
            if (i, j) in revealed:
                display += field[i][j] + " "
            else:
                display += "⬜ "
        display += "\n"
    return display

async def calculate_stars_result(msg, field, revealed):
    found_bomb = any(field[i][j] == "💣" for i, j in revealed)
    found_stars = sum(1 for i, j in revealed if field[i][j] == "⭐")

    if found_bomb:
        await DB.execute("UPDATE users SET balance = balance - 10, total_games = total_games + 1 WHERE telegram_id = $1", msg.from_user.id)
        return "💥 Вы нашли бомбу! -10 от баланса."
    elif found_stars > 0:
        reward = found_stars * 10
        await DB.execute("UPDATE users SET balance = balance + $1, total_games = total_games + 1, vin_games = vin_games + 1 WHERE telegram_id = $2", reward, msg.from_user.id)
        return f"⭐ Вы нашли {found_stars} звезд(ы). +{reward} к балансу!"
    else:
        return "Игра завершена."