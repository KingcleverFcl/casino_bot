from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db import DB

router = Router()

class AuthState(StatesGroup):
    choose = State()
    nickname = State()
    password = State()

@router.message(F.text == "/start")
async def start_handler(msg: Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔑 У меня есть аккаунт")],
                  [KeyboardButton(text="🆕 Зарегистрироваться")]],
        resize_keyboard=True)
    await msg.answer("Привет! Выбери действие:", reply_markup=markup)
    await state.set_state(AuthState.choose)

@router.message(AuthState.choose, F.text == "🔑 У меня есть аккаунт")
async def login_step1(msg: Message, state: FSMContext):
    await msg.answer("Введите ник:")
    await state.set_state(AuthState.nickname)

@router.message(AuthState.choose, F.text == "🆕 Зарегистрироваться")
async def register_step1(msg: Message, state: FSMContext):
    await msg.answer("Придумайте ник:")
    await state.set_state(AuthState.nickname)

@router.message(AuthState.nickname)
async def input_password(msg: Message, state: FSMContext):
    await state.update_data(nickname=msg.text)
    await msg.answer("Введите пароль:")
    await state.set_state(AuthState.password)

@router.message(AuthState.password)
async def complete_auth(msg: Message, state: FSMContext):
    data = await state.get_data()
    nickname = data['nickname']
    password = msg.text

    user = await DB.fetchrow("SELECT * FROM users WHERE telegram_id = $1", msg.from_user.id)
    if user:
        await msg.answer("Вы уже вошли.")
    else:
        await DB.execute("INSERT INTO users (telegram_id, nickname, password) VALUES ($1, $2, $3)",
                         msg.from_user.id, nickname, password)
        await msg.answer("Успешная регистрация! Ваш баланс: 100")
    await state.clear()