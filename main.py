from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from db import BotDB

BotDB = BotDB('UsatuBot_Database.db')

bot = Bot(token='Токен_бота')
dp = Dispatcher(bot, storage=MemoryStorage())


class Step_data(StatesGroup):
    waiting = State()
    st_start = State()
    menu = State()
    to_menu = State()
    ex_del = State()
    dir_search = State()
    about_un = State()
    admission = State()
    dir_test = State()
    dir_test_1 = State()
    dir_test_2 = State()


def reg_inl_key():
    buttons = [types.InlineKeyboardButton(text="Математика", callback_data="ex_math"),
               types.InlineKeyboardButton(text="Русский язык", callback_data="ex_rus"),
               types.InlineKeyboardButton(text="Информатика", callback_data="ex_inf"),
               types.InlineKeyboardButton(text="Физика", callback_data="ex_phy"),
               types.InlineKeyboardButton(text="Обществознание", callback_data="ex_soc"),
               types.InlineKeyboardButton(text="Химия", callback_data="ex_chem")]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def menu_text():
    menu = "Добро пожаловать в меню! \n \nС помощью меню вы можете: \n▫️ Ознакомится с перечнем направлений обучения " \
           "в разделе «Перечень направлений». \n▫️ Получить информацию об университете, его факультетах, а также военной кафедре в разделе «Об " \
           "университете». \n▫️ Получить необходимую информацию о приемной компании можно в разделе «Поступление». \n▫️ " \
           "Добавлять и редактировать информацию о ваших экзаменах в разделе «Профиль абитуриента». \n▫️ Посмотреть " \
           "список направлений, куда можно поступить с вашими экзаменами в разделе «Возможные направления для вас». "
    return menu


def menu_key():
    buttons = ["Перечень направлений", "Об университете", "Поступление", "Профиль абитуриента",
               "Возможные направления для вас"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def profile_out(user_id):
    text = "Добро пожаловать в профиль абитуриента! \n \n Здесь вы можете посмотреть список ваших экзаменов, " \
           "а также добавить новые и удалить ненужные экзамены 📝\n "
    text += exam_out(user_id)
    return text


def exam_out(user_id):
    exams_def = BotDB.user_exam_out(user_id)
    if len(exams_def):
        numb = 1
        exams = "\n Ваши экзамены: \n"
        for i in range(len(exams_def)):
            exams += f" {numb}.   {exams_def[i]} \n"
            numb += 1
    else:
        exams = "\nВы не добавляли экзамены, для добавления экзаменов нажмите «Добавить экзамены» ☹️"
    return exams


def profile_inl_key():
    buttons = [types.InlineKeyboardButton(text="Добавить экзамены", callback_data="ex_add"),
               types.InlineKeyboardButton(text="Удалить экзамены", callback_data="ex_del")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def menu_dir_out():
    text = "Добро пожаловать в перечень направлений! \n \n Здесь вы можете посмотреть список направлений обучения для " \
           "бакалавриата и специалитета 📋 \n "
    return text


def dir_out():
    dir_def = BotDB.dir_out()
    direct = ["", "", "", "", ""]
    direct[0] = "\n Направления обучения: \n"
    j = 0
    i = 0
    while i < (len(dir_def)):
        while i < (len(dir_def)) and (len(direct[j])) < 3800:
            direct[
                j] += f"\n{dir_def[i + 1]}  {dir_def[i + 2]} \n📝 Необходимые экзамены: {dir_def[i + 3]}, {dir_def[i + 4]}, {dir_def[i + 5]}.\n✅ Проходной бал на бюджет прошлого года: {dir_def[i + 6]}\n"
            i += 7
        j += 1
    return direct


def dir_inl_key():
    buttons = [types.InlineKeyboardButton(text="Подробнее о направлениях...", callback_data="dir_search")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def opt_dir_inl_key():
    buttons = [types.InlineKeyboardButton(text="Подробнее о направлениях...", callback_data="dir_search"),
               types.InlineKeyboardButton(text="Подобрать направления по интересу...", callback_data="optimal_dir")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def dir_adv_inl_key():
    buttons = [types.InlineKeyboardButton(text="Подробнее о направлениях...", callback_data="dir_search"),
               types.InlineKeyboardButton(text="Перейти в меню", callback_data="dir_exit")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def to_menu_inl():
    buttons = [types.InlineKeyboardButton(text="Перейти в меню", callback_data="dir_exit")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def dir_water_out(value):
    dir_def = BotDB.dir_water_out(value)
    direct = ""
    i = 0
    while i < (len(dir_def)):
        direct += f"\n{dir_def[i]}"
        i += 1
    return direct


def dir_suitable_out(user_id):
    dir_def = BotDB.dir_rec_out(user_id)
    direct = ["", "", "", "", ""]
    direct[0] = "\nНаправления обучения, которые вам подходят: \n"
    j = 0
    i = 0
    while i < (len(dir_def)):
        while i < (len(dir_def)) and (len(direct[j])) < 3800:
            direct[
                j] += f"\n{dir_def[i + 1]}  {dir_def[i + 2]} \n📝 Необходимые экзамены: {dir_def[i + 3]}, {dir_def[i + 4]}, {dir_def[i + 5]}.\n✅ Проходной бал на бюджет прошлого года: {dir_def[i + 6]}\n"
            i += 7
        j += 1
    return direct


def about_text_gen():
    text = "✈️ УГАТУ – является одним из самых престижных вузов республики Башкортостан, а также состоит в числе самых " \
           "передовых технических вузов России.\n \nОб этом говорят оценки мировых репутационных рейтингов: " \
           "Шанхайского, RUR Reputation Rankings, Times Higher Education, проекта «Социальный навигатор» и др. Также " \
           "УГАТУ первым в России начал разработку программы электронной биржи труда для выпускников.\n \n🏢УГАТУ в " \
           "цифрах: \nБолее 16 тысяч студентов и аспирантов, более 1000 преподавателей, в том числе около 160 " \
           "докторов и 550 кандидатов наук."
    return text


def about_text_gen_1():
    text = "📚В УГАТУ располагаются 4 факультета, 2 института, а также военный учебный центр."
    return text


def about_inl_key():
    buttons = [types.InlineKeyboardButton(text="О факультетах", callback_data="about_fac"),
               types.InlineKeyboardButton(text="О военной кафедре", callback_data="about_arm"),
               types.InlineKeyboardButton(text="Перейти в меню", callback_data="about_exit")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def about_fac_inl_key():
    buttons = [types.InlineKeyboardButton(text="О военной кафедре", callback_data="about_arm"),
               types.InlineKeyboardButton(text="Перейти в меню", callback_data="about_exit")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def about_arm_inl_key():
    buttons = [types.InlineKeyboardButton(text="О факультетах", callback_data="about_fac"),
               types.InlineKeyboardButton(text="Перейти в меню", callback_data="about_exit")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def about_fac_out():
    about_def = BotDB.about_fac_out()
    about = ["", "", "", "", "", "", ""]
    about[0] = "\nПодробнее о факультетах:\n"
    i = 0
    while i < (len(about_def)):
        about[i] += f"\n{about_def[i]}"
        i += 1
    return about


def about_arm_out():
    about_def = BotDB.about_arm_out()
    about = ["", "", ""]
    about[0] = "\nПодробнее о военной кафедре:\n"
    i = 0
    while i < (len(about_def)):
        about[i] += f"\n{about_def[i]}\n"
        i += 1
    return about


def about_ad_key():
    buttons = ["Необходимые документы", "Сроки и график приема", "Как поступить?", "Бюджетное обучение",
               "Целевое обучение", "Платное обучение", "Перейти в меню"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def about_ad_text():
    text = "Добро пожаловать в раздел поступление!\n \nВ данном разделе вы найдете всю необходимую информацию о " \
           "процессе поступления в УГАТУ. \n" \
           "\n📝 Получить информацию о документах необходимых для поступления вы можете в пункте «Необходимые " \
           "документы\n \n🕑 Узнать о сроках, и графике работы приемной комиссии вы можете в пункте «Сроки и график " \
           "приема»\n \n❓ Узнать о том, как проходит поступление, вы можете в пункте «Как поступить?»\n \n🏛 Получить " \
           "информацию о бюджетной форме обучения вы можете в пункте «Бюджетное обучение»\n \n🔧 Получить информацию " \
           "о целевой форме обучения вы можете в пункте «Целевое обучение»\n \n💵 Получить информацию о платном " \
           "обучении вы можете в пункте «Платное обучение» "
    return text


def about_add_out(value):
    about_def = BotDB.about_admission(value)
    about = ""
    for i in range(len(about_def)):
        about += f"{about_def[i]}\n"
    return about


@dp.message_handler(commands="start", state="*")
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    start_message = 'Привет, я УГАТУ.bot 👋 \n'
    start_message += '\nС моей помощью Вы сможете найти ответы на интересующие вопросы касательно поступления, ' \
                     'подобрать направления обучения которые вам подходят и многое другое 🔥 \n '
    start_message += '\nХотите ли вы ввести список своих экзаменов?'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Ввести экзамены", "Перейти в меню"]
    keyboard.add(*buttons)
    await message.answer(start_message, reply_markup=keyboard)
    await Step_data.st_start.set()


@dp.message_handler(state=Step_data.st_start, content_types=types.ContentTypes.TEXT)
async def step_start(message: types.Message):
    dp.message_handler(content_types=['text'])
    answ = message.text
    if answ == "Ввести экзамены":
        await message.answer('Выберите экзамены, которые вы сдавали:', reply_markup=reg_inl_key())
        await Step_data.to_menu.set()
    elif answ == "Перейти в меню":
        await message.answer(menu_text(), reply_markup=menu_key())
        await Step_data.menu.set()
    else:
        await message.answer('Я так не умею, выбери вариант из кнопок!')
        await Step_data.st_start.set()


@dp.message_handler(state=Step_data.to_menu, content_types=types.ContentTypes.TEXT)
async def step_start(message: types.Message):
    dp.message_handler(content_types=['text'])
    answ = message.text
    if answ == "Перейти в меню":
        await message.answer(menu_text(), reply_markup=menu_key())
        await Step_data.menu.set()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton(text="Перейти в меню")
        keyboard.add(button)
        await message.answer("После введения экзаменов вы можете перейти в меню.", reply_markup=keyboard)
        await Step_data.to_menu.set()


@dp.callback_query_handler(text="ex_math", state=Step_data.to_menu)
async def send_math(call: types.CallbackQuery):
    value = "Математика"
    if (BotDB.user_exam_exists(call.from_user.id, value)) < 1:
        BotDB.add_record(call.from_user.id, value)
        await call.answer(text="Математика добавлена в список ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже добавили математику в список ваших экзаменов!")
    # await call.answer(text="Что-то пошло не так.. Попробуйте позже.", show_alert=True)


@dp.callback_query_handler(text="ex_rus", state=Step_data.to_menu)
async def send_rus(call: types.CallbackQuery):
    value = "Русский язык"
    if (BotDB.user_exam_exists(call.from_user.id, value)) < 1:
        BotDB.add_record(call.from_user.id, value)
        await call.answer(text="Русский язык добавлен в список ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже добавили русский язык в список ваших экзаменов!")


@dp.callback_query_handler(text="ex_inf", state=Step_data.to_menu)
async def send_inf(call: types.CallbackQuery):
    value = "Информатика"
    if (BotDB.user_exam_exists(call.from_user.id, value)) < 1:
        BotDB.add_record(call.from_user.id, value)
        await call.answer(text="Информатика добавлена в список ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже добавили информатику в список ваших экзаменов!")


@dp.callback_query_handler(text="ex_phy", state=Step_data.to_menu)
async def send_phy(call: types.CallbackQuery):
    value = "Физика"
    if (BotDB.user_exam_exists(call.from_user.id, value)) < 1:
        BotDB.add_record(call.from_user.id, value)
        await call.answer(text="Физика добавлена в список ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже добавили физику в список ваших экзаменов!")


@dp.callback_query_handler(text="ex_soc", state=Step_data.to_menu)
async def send_soc(call: types.CallbackQuery):
    value = "Обществознание"
    if (BotDB.user_exam_exists(call.from_user.id, value)) < 1:
        BotDB.add_record(call.from_user.id, value)
        await call.answer(text="Обществознание добавлено в список ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже добавили обществознание в список ваших экзаменов!")


@dp.callback_query_handler(text="ex_chem", state=Step_data.to_menu)
async def send_chem(call: types.CallbackQuery):
    value = "Химия"
    if (BotDB.user_exam_exists(call.from_user.id, value)) < 1:
        BotDB.add_record(call.from_user.id, value)
        await call.answer(text="Химия добавлена в список ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже добавили Химию в список ваших экзаменов!")


@dp.message_handler(state=Step_data.menu, content_types=types.ContentTypes.TEXT)
async def step_menu(message: types.Message):
    dp.message_handler(content_types=['text'])
    answ = message.text
    if answ == "Профиль абитуриента":
        await message.answer(profile_out(message.from_user.id), reply_markup=profile_inl_key())
    elif answ == "Перечень направлений":
        await message.answer(menu_dir_out())
        text_dir = dir_out()
        for i in range(len(text_dir)):
            if len(text_dir[i]) > 0:
                await message.answer(text_dir[i], reply_markup=dir_inl_key())
    elif answ == "Об университете":
        await message.answer(about_text_gen(), reply_markup=types.ReplyKeyboardRemove())
        await message.answer(about_text_gen_1(), reply_markup=about_inl_key())
        await Step_data.about_un.set()
    elif answ == "Поступление":
        await message.answer(about_ad_text(), reply_markup=about_ad_key())
        await Step_data.admission.set()
    elif answ == "Возможные направления для вас":
        if BotDB.dir_rec_exist(message.from_user.id):
            suitable_dir = dir_suitable_out(message.from_user.id)
            for i in range(len(suitable_dir)):
                if len(suitable_dir[i]) > 0:
                    await message.answer(suitable_dir[i], reply_markup=opt_dir_inl_key())
        elif 1 <= BotDB.user_exam_check(message.from_user.id) < 3:
            await message.answer("Ваших экзаменов недостаточно ни для одного из направлений обучения, для поступления "
                                 "необходимо минимум 3 экзамена 🙃\n \n❓ Чтобы добавить экзамены перейдите в раздел "
                                 "«Профиль абитуриента»", reply_markup=menu_key())
        elif BotDB.user_exam_check(message.from_user.id) == 0:
            await message.answer(
                "Вы не добавили ни одного экзамена 🤕 \nЧтобы воспользоваться функцией добавьте экзамены "
                "в разделе «Профиль абитуриента»", reply_markup=menu_key())
        else:
            await message.answer("Сожалеем, но мы не нашли ни одного подходящего вам направления 😢",
                                 reply_markup=menu_key())
    else:
        await message.answer('Я так не умею, выбери вариант из кнопок!')


@dp.callback_query_handler(text="ex_add", state=Step_data.menu)
async def add_ex(call: types.CallbackQuery):
    await call.message.answer('Выберите экзамены, которые вы сдавали:', reply_markup=reg_inl_key())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Перейти в меню")
    keyboard.add(button)
    await call.message.answer("Для выхода в меню, нажмите\n«Перейти в меню»", reply_markup=keyboard)
    await Step_data.to_menu.set()


@dp.callback_query_handler(text="ex_del", state=Step_data.menu)
async def del_ex(call: types.CallbackQuery):
    await call.message.answer('Выберите экзамены, которые вы хотите удалить:', reply_markup=reg_inl_key())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Перейти в меню")
    keyboard.add(button)
    await call.message.answer("Для выхода в меню, нажмите\n«Перейти в меню»", reply_markup=keyboard)
    await Step_data.ex_del.set()


@dp.callback_query_handler(text="ex_math", state=Step_data.ex_del)
async def del_math(call: types.CallbackQuery):
    value = "Математика"
    if (BotDB.user_exam_exists(call.from_user.id, value)) >= 1:
        BotDB.del_record(call.from_user.id, value)
        await call.answer(text="Математика удалена из списка ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже удалили математику из списка ваших экзаменов!")


@dp.callback_query_handler(text="ex_rus", state=Step_data.ex_del)
async def del_rus(call: types.CallbackQuery):
    value = "Русский язык"
    if (BotDB.user_exam_exists(call.from_user.id, value)) >= 1:
        BotDB.del_record(call.from_user.id, value)
        await call.answer(text="Русский язык удален из списка ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже удалили русский язык из списка ваших экзаменов!")


@dp.callback_query_handler(text="ex_inf", state=Step_data.ex_del)
async def del_inf(call: types.CallbackQuery):
    value = "Информатика"
    if (BotDB.user_exam_exists(call.from_user.id, value)) >= 1:
        BotDB.del_record(call.from_user.id, value)
        await call.answer(text="Информатика удалена из списка ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже удалили информатику из списка ваших экзаменов!")


@dp.callback_query_handler(text="ex_phy", state=Step_data.ex_del)
async def del_phy(call: types.CallbackQuery):
    value = "Физика"
    if (BotDB.user_exam_exists(call.from_user.id, value)) >= 1:
        BotDB.del_record(call.from_user.id, value)
        await call.answer(text="Физика удалена из списка ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже удалили физику из списка ваших экзаменов!")


@dp.callback_query_handler(text="ex_soc", state=Step_data.ex_del)
async def del_soc(call: types.CallbackQuery):
    value = "Обществознание"
    if (BotDB.user_exam_exists(call.from_user.id, value)) >= 1:
        BotDB.del_record(call.from_user.id, value)
        await call.answer(text="Обществознание удалено из списка ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже удалили обществознание из списка ваших экзаменов!")


@dp.callback_query_handler(text="ex_chem", state=Step_data.ex_del)
async def del_chem(call: types.CallbackQuery):
    value = "Химия"
    if (BotDB.user_exam_exists(call.from_user.id, value)) >= 1:
        BotDB.del_record(call.from_user.id, value)
        await call.answer(text="Химия удалена из списка ваших экзаменов!", show_alert=True)
    else:
        await call.answer(text="Вы уже удалили Химию из списка ваших экзаменов!")


@dp.message_handler(state=Step_data.ex_del, content_types=types.ContentTypes.TEXT)
async def step_start(message: types.Message):
    dp.message_handler(content_types=['text'])
    answ = message.text
    if answ == "Перейти в меню":
        await message.answer(menu_text(), reply_markup=menu_key())
        await Step_data.menu.set()
    else:
        await message.answer('Я так не умею, выбери вариант из кнопок!')


@dp.callback_query_handler(text="dir_search", state=Step_data.menu)
async def dir_call(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Перейти в меню")
    keyboard.add(button)
    await call.message.answer('Введите код интересующего направления, прим. «09.03.01»', reply_markup=keyboard)
    await Step_data.dir_search.set()


@dp.message_handler(state=Step_data.dir_search, content_types=types.ContentTypes.TEXT)
async def dir_search(message: types.Message):
    dp.message_handler(content_types=['text'])
    answ = message.text
    if (BotDB.dir_exists(answ)) == 1:
        await message.answer(text=dir_water_out(answ), reply_markup=dir_adv_inl_key())
    elif answ == "Перейти в меню":
        await message.answer(menu_text(), reply_markup=menu_key())
        await Step_data.menu.set()
    else:
        await message.answer('Нет такого направления!', reply_markup=dir_adv_inl_key())


@dp.callback_query_handler(text="dir_exit", state=Step_data.dir_search)
async def dir_call_exit(call: types.CallbackQuery):
    await call.message.answer(menu_text(), reply_markup=menu_key())
    await Step_data.menu.set()


@dp.callback_query_handler(text="about_fac", state=Step_data.about_un)
async def abot_fac(call: types.CallbackQuery):
    text_dir = about_fac_out()
    for i in range(len(text_dir)):
        if len(text_dir[i]) > 0:
            if i + 1 == len(text_dir):
                await call.message.answer(text_dir[i], reply_markup=about_fac_inl_key())
            else:
                await call.message.answer(text_dir[i], reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text="about_arm", state=Step_data.about_un)
async def about_arm(call: types.CallbackQuery):
    text_dir = about_arm_out()
    for i in range(len(text_dir)):
        if len(text_dir[i]) > 0:
            if i + 1 == len(text_dir):
                await call.message.answer(text_dir[i], reply_markup=about_arm_inl_key())
            else:
                await call.message.answer(text_dir[i], reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text="about_exit", state=Step_data.about_un)
async def about_exit(call: types.CallbackQuery):
    await call.message.answer(menu_text(), reply_markup=menu_key())
    await Step_data.menu.set()


@dp.message_handler(state=Step_data.admission, content_types=types.ContentTypes.TEXT)
async def about_ad_menu(message: types.Message):
    dp.message_handler(content_types=['text'])
    answ = message.text
    if answ == "Перейти в меню":
        await message.answer(menu_text(), reply_markup=menu_key())
        await Step_data.menu.set()
    elif answ == "Необходимые документы":
        value = 3
        text_dir = about_add_out(value)
        await message.answer(text_dir, reply_markup=about_ad_key())
    elif answ == "Сроки и график приема":
        value = 4
        text_dir = about_add_out(value)
        await message.answer(text_dir, reply_markup=about_ad_key())
    elif answ == "Как поступить?":
        value = 5
        text_dir = about_add_out(value)
        await message.answer(text_dir, reply_markup=about_ad_key())
    elif answ == "Бюджетное обучение":
        value = 6
        text_dir = about_add_out(value)
        await message.answer(text_dir, reply_markup=about_ad_key())
    elif answ == "Целевое обучение":
        value = 7
        text_dir = about_add_out(value)
        await message.answer(text_dir, reply_markup=about_ad_key())
    elif answ == "Платное обучение":
        value = 8
        text_dir = about_add_out(value)
        await message.answer(text_dir, reply_markup=about_ad_key())
    else:
        await message.answer('Я так не умею, выбери вариант из кнопок!')


def test_err_1():
    text = "Сожалеем, но для направлений с вашими экзаменами, данная функция недоступна 😢 \n \nДанная функция " \
           "доступна только для направлений с экзаменом «Информатика» 💻 "
    return text


def test_err_2():
    text = "Сожалеем, но данная функция данная функция доступна только для направлений с экзаменом «Информатика» 😢 " \
           "\n \n "
    return text


def test_err_inl_key():
    buttons = [types.InlineKeyboardButton(text="Начать тест..", callback_data="test_comp")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def test_0():
    text = "Вы начали начали тест, для направлений с экзаменом «Информатика» 💻"
    return text


def test_1():
    text = "Что вам более интересно, " \
           "железо или программное обеспечение? "
    return text


def test_21():
    text = "Вас привлекает разработка компонентов (микропроцессоров, контроллеров и пр.) или разработка систем (" \
           "станки, роботы и пр.)? "
    return text


def test_22():
    text = "Что привлекает вас больше, программирование или защита информации?"
    return text


def test_23():
    text = "Вы хотите работать с «ПО» или его разрабатывать?"
    return text


def test_3():
    text = "Вы хотите программировать или проектировать «ПО»?"
    return text


def test_1_inl_key():
    buttons = [types.InlineKeyboardButton(text="«ПО»", callback_data="test_po"),
               types.InlineKeyboardButton(text="И то, и другое", callback_data="test_all"),
               types.InlineKeyboardButton(text="«Железо»", callback_data="test_metal")]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def test_21_inl_key():
    buttons = [types.InlineKeyboardButton(text="Компонентов", callback_data="test_comp"),
               types.InlineKeyboardButton(text="Систем", callback_data="test_sys")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def test_22_inl_key():
    buttons = [types.InlineKeyboardButton(text="программирование", callback_data="test_prg"),
               types.InlineKeyboardButton(text="Защита информации", callback_data="test_zi")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def test_23_inl_key():
    buttons = [types.InlineKeyboardButton(text="Работать", callback_data="test_wor"),
               types.InlineKeyboardButton(text="Разрабатывать", callback_data="test_dev")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def test_3_inl_key():
    buttons = [types.InlineKeyboardButton(text="Программировать", callback_data="test_prog"),
               types.InlineKeyboardButton(text="Проектировать", callback_data="test_proect")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def test_dir_out(user_id):
    dir_def = BotDB.user_dir_out(user_id)
    direct = ["", "", "", "", ""]
    direct[0] = "💡 Перечень направлений подходящих вашим интересам: \n"
    j = 0
    i = 0
    while i < (len(dir_def)):
        while i < (len(dir_def)) and (len(direct[j])) < 3800:
            direct[
                j] += f"\n{dir_def[i + 1]}  {dir_def[i + 2]} \n📝 Необходимые экзамены: {dir_def[i + 3]}, {dir_def[i + 4]}, {dir_def[i + 5]}.\n✅ Проходной бал на бюджет прошлого года: {dir_def[i + 6]}\n"
            i += 7
        j += 1
    return direct


def opt_dir_adv_inl_key():
    buttons = [types.InlineKeyboardButton(text="Подробнее о направлениях...", callback_data="dir_search"),
               types.InlineKeyboardButton(text="Подобррать направления заново...", callback_data="optimal_dir_restart")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


@dp.callback_query_handler(text="optimal_dir_restart", state=Step_data.menu)
async def opt_dir_rest_call(call: types.CallbackQuery):
    value = ''
    BotDB.user_dir_add(call.from_user.id, value)
    if BotDB.user_dir_flag_out(call.from_user.id) == [None] or BotDB.user_dir_flag_out(call.from_user.id) == ['']:
        if BotDB.user_exam_check(call.from_user.id) == 3:
            if "Информатика" in BotDB.user_exam_out(call.from_user.id):
                await call.message.answer(test_0(), reply_markup=types.ReplyKeyboardRemove())
                await call.message.answer(test_1(), reply_markup=test_1_inl_key())
                await Step_data.dir_test.set()
            else:
                await call.message.answer(test_err_1())
        else:
            await call.message.answer(test_err_2(), reply_markup=types.ReplyKeyboardRemove())
            text = ""
            text += f'{test_0()}\n \n{test_1()}'
            await call.message.answer(text, reply_markup=test_1_inl_key())
            await Step_data.dir_test.set()


@dp.callback_query_handler(text="optimal_dir", state=Step_data.menu)
async def opt_dir_call(call: types.CallbackQuery):
    if BotDB.user_dir_flag_out(call.from_user.id) == [None] or BotDB.user_dir_flag_out(call.from_user.id) == ['']:
        if BotDB.user_exam_check(call.from_user.id) == 3:
            if "Информатика" in BotDB.user_exam_out(call.from_user.id):
                await call.message.answer(test_0(), reply_markup=types.ReplyKeyboardRemove())
                await call.message.answer(test_1(), reply_markup=test_1_inl_key())
                await Step_data.dir_test.set()
            else:
                await call.message.answer(test_err_1())
        else:
            await call.message.answer(test_err_2(), reply_markup=types.ReplyKeyboardRemove())
            text = ""
            text += f'{test_0()}\n \n{test_1()}'
            await call.message.answer(text, reply_markup=test_1_inl_key())
            await Step_data.dir_test.set()
    else:
        suitable_dir = test_dir_out(call.from_user.id)
        for i in range(len(suitable_dir)):
            if len(suitable_dir[i]) > 0:
                await call.message.answer(suitable_dir[i], reply_markup=opt_dir_adv_inl_key())


@dp.callback_query_handler(text="test_metal", state=Step_data.dir_test)
async def opt_dir_call_1(call: types.CallbackQuery):
    await call.message.answer(test_21(), reply_markup=test_21_inl_key())
    await Step_data.dir_test_1.set()


@dp.callback_query_handler(text="test_all", state=Step_data.dir_test)
async def opt_dir_call_2(call: types.CallbackQuery):
    await call.message.answer(test_22(), reply_markup=test_22_inl_key())
    await Step_data.dir_test_1.set()


@dp.callback_query_handler(text="test_po", state=Step_data.dir_test)
async def opt_dir_call_3(call: types.CallbackQuery):
    await call.message.answer(test_23(), reply_markup=test_23_inl_key())
    await Step_data.dir_test_1.set()


@dp.callback_query_handler(text="test_dev", state=Step_data.dir_test_1)
async def opt_dir_call_4(call: types.CallbackQuery):
    await call.message.answer(test_3(), reply_markup=test_3_inl_key())
    await Step_data.dir_test_2.set()


@dp.callback_query_handler(text="test_prog", state=Step_data.dir_test_2)
async def opt_dir_call_5(call: types.CallbackQuery):
    value = "B"
    BotDB.user_dir_add(call.from_user.id, value)
    suitable_dir = test_dir_out(call.from_user.id)
    for i in range(len(suitable_dir)):
        if len(suitable_dir[i]) > 0:
            await call.message.answer(suitable_dir[i], reply_markup=dir_adv_inl_key())
    await Step_data.menu.set()


@dp.callback_query_handler(text="test_proect", state=Step_data.dir_test_2)
async def opt_dir_call_6(call: types.CallbackQuery):
    value = "C"
    BotDB.user_dir_add(call.from_user.id, value)
    suitable_dir = test_dir_out(call.from_user.id)
    for i in range(len(suitable_dir)):
        if len(suitable_dir[i]) > 0:
            await call.message.answer(suitable_dir[i], reply_markup=dir_adv_inl_key())
    await Step_data.menu.set()


@dp.callback_query_handler(text="test_wor", state=Step_data.dir_test_1)
async def opt_dir_call_7(call: types.CallbackQuery):
    value = "A"
    BotDB.user_dir_add(call.from_user.id, value)
    suitable_dir = test_dir_out(call.from_user.id)
    for i in range(len(suitable_dir)):
        if len(suitable_dir[i]) > 0:
            await call.message.answer(suitable_dir[i], reply_markup=dir_adv_inl_key())
    await Step_data.menu.set()


@dp.callback_query_handler(text="test_zi", state=Step_data.dir_test_1)
async def opt_dir_call_8(call: types.CallbackQuery):
    value = "E"
    BotDB.user_dir_add(call.from_user.id, value)
    suitable_dir = test_dir_out(call.from_user.id)
    for i in range(len(suitable_dir)):
        if len(suitable_dir[i]) > 0:
            await call.message.answer(suitable_dir[i], reply_markup=dir_adv_inl_key())
    await Step_data.menu.set()


@dp.callback_query_handler(text="test_prg", state=Step_data.dir_test_1)
async def opt_dir_call_9(call: types.CallbackQuery):
    value = "D"
    BotDB.user_dir_add(call.from_user.id, value)
    suitable_dir = test_dir_out(call.from_user.id)
    for i in range(len(suitable_dir)):
        if len(suitable_dir[i]) > 0:
            await call.message.answer(suitable_dir[i], reply_markup=dir_adv_inl_key())
    await Step_data.menu.set()


@dp.callback_query_handler(text="test_sys", state=Step_data.dir_test_1)
async def opt_dir_call_10(call: types.CallbackQuery):
    value = "G"
    BotDB.user_dir_add(call.from_user.id, value)
    suitable_dir = test_dir_out(call.from_user.id)
    for i in range(len(suitable_dir)):
        if len(suitable_dir[i]) > 0:
            await call.message.answer(suitable_dir[i], reply_markup=dir_adv_inl_key())
    await Step_data.menu.set()


@dp.callback_query_handler(text="test_comp", state=Step_data.dir_test_1)
async def opt_dir_call_11(call: types.CallbackQuery):
    value = "F"
    BotDB.user_dir_add(call.from_user.id, value)
    suitable_dir = test_dir_out(call.from_user.id)
    for i in range(len(suitable_dir)):
        if len(suitable_dir[i]) > 0:
            await call.message.answer(suitable_dir[i], reply_markup=dir_adv_inl_key())
    await Step_data.menu.set()


@dp.callback_query_handler(text="dir_exit", state=Step_data.menu)
async def dir_call_exit(call: types.CallbackQuery):
    await call.message.answer(menu_text(), reply_markup=menu_key())
    await Step_data.menu.set()


executor.start_polling(dp)
