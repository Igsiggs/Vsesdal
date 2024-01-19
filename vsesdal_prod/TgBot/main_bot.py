from django.conf import settings
from telebot import TeleBot, types
from keyboa.keyboard import Keyboa
from TgBot.models import Executor, OptionsTgBot
from Orders.models import Orders
import datetime
import os

bot = TeleBot(settings.BOT_TOKEN, parse_mode='HTML')
back_page = ''
id_order_ = 0
index_order = 0
complete_order = 0


@bot.message_handler(['start', 'restart'])
def send_welcome(message):
    # print(type(message))
    bot.delete_message(message.chat.id, message.id)
    # print(message.from_user.username)
    try:
        Executor.objects.get(tg_name=message.from_user.username)

    except:
        a = Executor(external_id=message.id,
                     tg_name=message.from_user.username,
                     balance=0,
                     role=1,
                     orders_finish='',
                     orders_in_progress='',
                     )
        a.save()
    options = OptionsTgBot.objects.all().values_list('values', named=True).get(options='Приветствие')
    text_greet = list(options)[0].split('[')[0]
    # print(eval(list(options)[0].split('\n')[2]))
    keyboard = Keyboa(items=eval(list(options)[0].split('\n')[2]), items_in_row=3, copy_text_to_callback=True)
    bot.send_message(message.chat.id, text_greet, reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: call.data == 'Помощь')
def help(call):
    global back_page
    back_page = 'send_welcome(call.message)'
    try:
        for i in range(10):
            bot.delete_message(call.message.chat.id, call.message.id - i)
    except:
        markup = Keyboa(items=['Назад'], items_in_row=1, copy_text_to_callback=True)
        bot.send_contact(call.message.chat.id, '+79959069468', 'Helper', reply_markup=markup())


@bot.callback_query_handler(func=lambda call: call.data == 'Назад')
def back(call):
    global back_page
    eval(back_page)


def list_orders(index):
    values = Orders.objects.all().values_list(
        'id_order',
        'title',
        'categories',
        'price',
        'deadline',
        'antiplug',
        'text',
        named=True).filter(status='Новый')
    value_ = list(values)
    try:
        global id_order_
        value_[index] = list(value_[index])
        value_[index][3] *= float(list(OptionsTgBot.objects.all().values_list(
            'values',
            named=True).get(options='Процент стоимости'))[0])
        id_order_ = value_[index][0]
        # print(id_order_)
        # print(value_[index])
        options = OptionsTgBot.objects.all().values_list('values', named=True).get(options='Найти Заказ')

        # print(id_order_)
        # print(list(options)[0].split('[')[0].format(*list(values)[1::]))
        text = list(options)[0].split('[')[0].format(*value_[index][1::])

        # print(list(options)[0].split('\n'))

        markup = Keyboa(items=eval(list(options)[0].split('\n')[10]), items_in_row=2, copy_text_to_callback=True)
        return text, markup
    except Exception as ex:
        print(ex)
        text = 'Это все заказы!'
        markup = Keyboa(items=[('Окей', 'Назад')], items_in_row=1)
        global index_order
        index_order = 0
        return text, markup


@bot.callback_query_handler(func=lambda call: call.data == 'Найти Заказы')
def find_orders(call):
    global back_page
    back_page = 'send_welcome(call.message)'
    bot.delete_message(call.message.chat.id, call.message.id)
    global index_order
    text, markup = list_orders(index_order)
    bot.send_message(call.message.chat.id, text, reply_markup=markup())


@bot.callback_query_handler(func=lambda call: call.data == 'Отклонить')
def reject(call):
    global index_order
    index_order += 1
    find_orders(call)


@bot.callback_query_handler(func=lambda call: call.data == 'Взять')
def accept(call):
    global back_page, id_order_
    back_page = 'send_welcome(call.message)'
    try:
        executor = Executor.objects.get(tg_name=call.from_user.username)
        print(executor.orders_in_progress)
        if executor.orders_in_progress == '':
            executor.orders_in_progress += '{id}'.format(id=id_order_)
        else:
            executor.orders_in_progress += ',{id}'.format(id=id_order_)
        print(executor.orders_in_progress)
        executor.save()
        order = Orders.objects.get(id_order=id_order_)
        print(order.status)
        order.status = 'В работе'
        order.save()
        bot.delete_message(call.message.chat.id, call.message.id)
        text = 'Закаказ добавлен в ваши заказы'
        markup = Keyboa(items=['Мои Заказы', 'Назад'], items_in_row=2, copy_text_to_callback=True)
        bot.send_message(call.message.chat.id, text, reply_markup=markup())
    except Exception as ex:
        print(ex)
        bot.delete_message(call.message.chat.id, call.message.id)
        markup = Keyboa(items=[('Окей', 'Назад')], items_in_row=1)
        bot.send_message(call.message.chat.id, 'Извините попробуйте ещё раз)', reply_markup=markup())


@bot.callback_query_handler(func=lambda call: call.data == 'Кабинет')
def cabinet(call):
    global back_page
    back_page = 'send_welcome(call.message)'
    # print(call.from_user.username)
    values = Executor.objects.all().values_list(
        'tg_name',
        'role',
        'balance',
        'orders_finish',
        'orders_in_progress',
        named=True).get(tg_name=call.from_user.username)
    # print(list(values))
    options = OptionsTgBot.objects.all().values_list('values', named=True).get(options='Личный кабинет')
    # print(list(values)[:3:])
    # print(list(options))

    text = list(options)[0].split('[')[0].format(*list(values)[:3:])
    print(list(values)[:3:])
    markup = Keyboa(items=eval(list(options)[0].split('\n')[3]), items_in_row=1, copy_text_to_callback=True)
    # print(list(options)[0].split('[')[0].format(*list(values)[:3:]))
    # print(list(options)[0].format(*values))
    # print(call)
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, text, reply_markup=markup())


@bot.callback_query_handler(func=lambda call: call.data == 'Мои Заказы')
def menu_orders(call):
    try:
        global back_page
        back_page = 'send_welcome(call.message)'
        options = list(OptionsTgBot.objects.all().values_list('values').get(options='Мои Заказы'))[0].split('\n')
        print(options[1])
        markup = Keyboa(items=eval(options[1]) + ['Назад'], items_in_row=1, copy_text_to_callback=True)
        text = options[0]

        try:
            for i in range(10):
                bot.delete_message(call.message.chat.id, call.message.id - i)
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=markup())
    except Exception as ex:
        bot.delete_message(call.message.chat.id, call.message.id)
        markup = Keyboa(items=['Назад'], items_in_row=1, copy_text_to_callback=True)
        bot.send_message(call.message.chat.id, 'Попробуйте еще раз!', reply_markup=markup())
        print(ex)


@bot.callback_query_handler(func=lambda call: call.data == 'В РАБОТЕ')
def orders_in_progress(call):
    try:
        global back_page
        back_page = 'menu_orders(call)'

        id_orders_list = Executor.objects.all().values_list('orders_in_progress').get(tg_name=call.from_user.username)
        print(id_orders_list)
        list_executor_orders = Orders.objects.all().values_list().filter(
            id_order__in=list(map(int, (id_orders_list[0].split(',')))))
        print(list(list_executor_orders))
        # print([i[2] for i in list(list_executor_orders)] + 'Назад')
        markup = Keyboa(items=[i[2] for i in list(list_executor_orders)] + ['Назад'], items_in_row=1,
                        copy_text_to_callback=True)
        text = OptionsTgBot.objects.all().values_list('values').get(options='В РАБОТЕ')[0]
        print(text)
        print(markup)
        try:
            for i in range(10):
                bot.delete_message(call.message.chat.id, call.message.id - i)
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=markup())
    except Exception as ex:
        bot.delete_message(call.message.chat.id, call.message.id)
        markup = Keyboa(items=['Назад'], items_in_row=1, copy_text_to_callback=True)
        bot.send_message(call.message.chat.id, 'У вас нет заказов!', reply_markup=markup())
        print(ex)


@bot.callback_query_handler(func=lambda call: call.data == 'ВЫПОЛНЕННЫЕ')
def executor_orders_finish(call):
    try:
        global back_page
        back_page = 'menu_orders(call)'

        id_orders_list = Executor.objects.all().values_list('orders_finish').get(tg_name=call.from_user.username)
        print(id_orders_list)
        list_executor_orders = Orders.objects.all().values_list().filter(
            id_order__in=list(map(int, (id_orders_list[0].split(',')))))
        print(list(list_executor_orders))
        # print([i[2] for i in list(list_executor_orders)] + 'Назад')
        markup = Keyboa(items=[i[2] for i in list(list_executor_orders)] + ['Назад'], items_in_row=1,
                        copy_text_to_callback=True)
        text = OptionsTgBot.objects.all().values_list('values').get(options='ВЫПОЛНЕННЫЕ')[0]
        print(text)
        print(markup)
        try:
            for i in range(10):
                bot.delete_message(call.message.chat.id, call.message.id - i)
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=markup())

    except Exception as ex:
        bot.delete_message(call.message.chat.id, call.message.id)
        markup = Keyboa(items=['Назад'], items_in_row=1, copy_text_to_callback=True)
        bot.send_message(call.message.chat.id, 'У вас нет выполненных заказов!', reply_markup=markup())
        print(ex)


@bot.callback_query_handler(func=lambda call: call.data == 'ОЖИДАЮЩИЕ')
def pending_orders(call):
    try:
        global back_page
        back_page = 'menu_orders(call)'

        id_orders_list = Executor.objects.all().values_list('orders_pending').get(tg_name=call.from_user.username)
        print(id_orders_list)
        list_executor_orders = Orders.objects.all().values_list().filter(
            id_order__in=list(map(int, (id_orders_list[0].split(',')))))
        # print(list(list_executor_orders))
        # print([i[2] for i in list(list_executor_orders)] + 'Назад')
        markup = Keyboa(items=[i[2] for i in list(list_executor_orders)] + ['Назад'], items_in_row=1,
                        copy_text_to_callback=True)
        text = OptionsTgBot.objects.all().values_list('values').get(options='ОЖИДАЮЩИЕ')[0]
        # print(text)
        # print(markup)
        try:
            for i in range(10):
                bot.delete_message(call.message.chat.id, call.message.id - i)
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=markup())
    except Exception as ex:
        bot.delete_message(call.message.chat.id, call.message.id)
        markup = Keyboa(items=['Назад'], items_in_row=1, copy_text_to_callback=True)
        bot.send_message(call.message.chat.id, 'У вас нет заказов которые ожидают подтверждения!',
                         reply_markup=markup())
        print(ex)


def list_id(call, b_arg=False):
    f = []
    try:
        b = [0, 0, 0]
        print('**************')
        c = Executor.objects.all().values_list('orders_in_progress', 'orders_pending', 'orders_finish', ).get(
            tg_name=call.from_user.username)  # ))]))
        print(c)

        for index, i in enumerate(c):
            if ',' in i:
                b[index] = list(map(int, i.split(',')))
            elif i == '':
                b[index] = []
            elif len(i) != 0:
                b[index] = int(i)

    except Exception as ex:
        print(ex)
        b = list(map(int, [0 if i == '' else i for i in list(
            (Executor.objects.all().values_list('orders_in_progress', 'orders_pending', 'orders_finish', )
             .get(tg_name=call.from_user.username)))]))
    print(b)
    for i in b:
        print(i)
        if type(i) is list:
            if i == []:
                f.append(0)
            elif len(i) != 0:
                for g in i:
                    f.append(g)
        else:
            f.append(i)
    # print(f)
    a = list(Orders.objects.all().values_list().filter(id_order__in=f))
    if b_arg:
        return b
    else:
        return a


@bot.callback_query_handler(func=lambda call: call.data in [i[2] for i in list_id(call, False)])
def order_in_work(call):
    try:
        markup = Keyboa(items=['Назад'])
        print(1)
        global back_page, complete_order
        back_page = 'orders_in_progress(call)'
        order = list(Orders.objects.all().values_list(
            'id_order',
            'title',
            'categories',
            'price',
            'deadline',
            'antiplug',
            'text',
            'files',
        ).get(title=call.data))
        order[3] *= float(list(OptionsTgBot.objects.all().values_list(
            'values',
            named=True).get(options='Процент стоимости'))[0])
        complete_order = str(list(order)[0])
        print(complete_order)
        options = OptionsTgBot.objects.all().values_list('values', named=True).get(options='Страница Заказа')
        # print(list(options)[0].split('\n')[9])
        # print(*list(order)[1:7:])
        # print(str(list(order)[0]))
        list_file = os.listdir('orders/orders/{id}'.format(id=str(list(order)[0])))
        # print(list_file)
        text = list(options)[0].split('[')[0].format(*list(order)[1:7:])
        print(2)
        id_list = list_id(call, True)
        print(3)
        print('-----------------')
        print(id_list[0])
        print(complete_order)
        a = [complete_order]
        if int(complete_order) == id_list[0] or id_list[0] in list(map(int, a)):
            back_page = 'orders_in_progress(call)'
            markup = Keyboa(items=eval(list(options)[0].split('\n')[9]), items_in_row=2, copy_text_to_callback=True)
        elif id_list[1] == int(complete_order) or id_list[1] in list(map(int, a)):
            back_page = 'pending_orders(call)'
            markup = Keyboa(items=['Назад'], items_in_row=2, copy_text_to_callback=True)
        elif int(complete_order) == id_list[2] or id_list[2] in list(map(int, a)):
            back_page = 'executor_orders_finish(call)'
            markup = Keyboa(items=['Назад'], items_in_row=2, copy_text_to_callback=True)
        else:
            pass
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, text)
        for index, i in enumerate(list_file):
            with open('orders/orders/{id}/{name}'.format(id=str(list(order)[0]), name=i), 'rb') as f:
                file = f.read()
            # print(i)
            if index == len(list_file) - 1:
                bot.send_document(call.message.chat.id, file, i, reply_markup=markup())
            else:
                bot.send_document(call.message.chat.id, file, i)

    except Exception as ex:
        print(ex)


@bot.callback_query_handler(func=lambda call: call.data == 'Выполнил')
def order_complete(call):
    global back_page
    back_page = 'orders_in_progress(call)'
    try:
        val = list(OptionsTgBot.objects.all().values_list('values').get(options='Страница Выполнения'))
        # print(val)
        # print(val[0].split('\n')[1])
        markup = Keyboa(items=eval(val[0].split('\n')[1]), items_in_row=1, copy_text_to_callback=True)
        text = val[0].split('\n')[0]

        try:
            for i in range(10):
                bot.delete_message(call.message.chat.id, call.message.id - i)
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=markup())
    except Exception as ex:
        print(ex)


@bot.message_handler(content_types=['document'])
def get_file(message):
    global back_page, complete_order
    back_page = 'menu_orders(call)'
    try:

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # print(downloaded_file)
        src = '/home/jora/PycharmProjects/vsesdal/vsesdal_prod/orders/finish/{id}/'.format(
            id=complete_order) + message.document.file_name
        try:
            os.makedirs('/home/jora/PycharmProjects/vsesdal/vsesdal_prod/orders/finish/{id}/'.format(id=complete_order))
            with open(src, 'w') as new_file:
                new_file.write(downloaded_file)
        except Exception as ex:
            print(ex)

        executor = Executor.objects.get(tg_name=message.from_user.username)
        exec_pend = executor.orders_pending
        if exec_pend == '':
            executor.orders_pending += '{id}'.format(id=complete_order)
        elif exec_pend != '' and complete_order not in exec_pend:
            executor.orders_pending += ',{id}'.format(id=complete_order)
        else:
            pass
        ord = executor.orders_in_progress
        if ',' in ord:
            executor.orders_in_progress = ord.split(',').remove(complete_order)
        else:
            executor.orders_in_progress = ''
        executor.save()

        try:
            for i in range(10):
                bot.delete_message(message.chat.id, message.id - i)
        except Exception as ex:
            print(ex)
            markup = Keyboa(items=['Кабинет', 'Назад'], items_in_row=2, copy_text_to_callback=True)
            bot.send_message(message.chat.id, 'Спасибо, задание отправлено заказчику', reply_markup=markup())
        # print(executor.orders_in_progress)
    except Excepetion as ex:
        print(ex)
