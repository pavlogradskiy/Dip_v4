
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from core import VkTools

class BotInterface():
    def __init__(self, comunity_token, acces_token):
        self.vk = vk_api.VkApi(token=comunity_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(acces_token)
        self.params = {}
        self.worksheets = []
        self.offset = 0

    def message_send(self, user_id, message, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,
                        'random_id': get_random_id()}
                       )

    def event_handler(self):
        longpull = VkLongPoll(self.bot)
        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg_to_me = event.text.lower()
                peer_id = event.user_id
                client = tools.get_profile_info(peer_id)[0]
                print(client)

                self_user_data.getlist = search_params(client)

                if msg_to_me == 'Привет':
                                    
                    self.message_send(peer_id, f'Привет, {client["first_name"]}')
                    if self_user_data.town == 0:
                        self.message_send(peer_id, f'{client["first_name"]}, для поиска недостаточно данных.\n'
                                                   f'Введите, пожалуйста город для поиска\n'
                                                   f'В формате: г Пузово')

                    elif self_user_data.age_from == 0:
                        self.message_send(peer_id, f'{client["first_name"]}, для поиска не хватает данных.\n'
                                                   f'Введите, пожалуйста интервал возраста для поиска\n'
                                                   f'В формате: 22-33')
                    else:
                        self.message_send(peer_id, f'Чтобы искать по анкетным данным,\n '
                                                   f'которые вы указали на странице ВК, \n '
                                                   f'введите: поиск \n')
                elif msg_to_me == 'поиск':
                    if self_user_data.town == 0 or self_user_data.age_from == 0:

                        self.message_send(peer_id, f'Для поиска недостаточно данных.\n'
                                                   f'{self_user_data} ')

                    else:
                        self.finder(self_user_data.getlist)
                        self.profiles_manager(peer_id)
                        self.message_send(peer_id, f'Если вам нужны другие анкеты по тем же параметрам, '
                                                   f'снова введите: поиск \n'
                                                   f'Чтобы остановить бота, напишите: стоп\n'
                                                   f'Чтобы изменить параметры поиска, напишите: далее')               
                    
                elif (msg_to_me.split(' '))[0] == 'г':
                    town = msg_to_me.split(' ')[1].capitalize()
                    new_city_id = tools.find_city_id(f'{town}')
                    self_user_data.town = town
                    self_user_data.city_id = new_city_id
                    print(self_user_data)

                    self.message_send(peer_id, f'Теперь введите  команду: далее')               

                elif ''.join(msg_to_me.split('-')).isdigit() and len(msg_to_me) == 5:
                    addition = msg_to_me.split('-')
                    self_user_data.age_from = addition[0]
                    self_user_data.age_to = addition[1]
                    print(self_user_data)
                    print(addition)

                    self.message_send(peer_id, f'Теперь введите  команду: далее')

                elif msg_to_me == 'далее':
                    if self_user_data.town == 0 or self_user_data.age_from == 0:
                        self.message_send(peer_id, f'Для поиска недостаточно данных.\n'
                                                   f'{self_user_data} ')

                    else:
                        self.message_send(peer_id,   self_user_data)

                        self.finder(self_user_data.getlist)
                        self.profiles_manager(peer_id)

                        self.message_send(peer_id, f'Доступные команды: далее, стоп, привет\n'
                                                   f'Команда "пуск" ищет только по анкетным данным в ВК,\n'
                                                   f'если все данные указаны в вашем аккаунте')

                elif msg_to_me == 'стоп':
                    break
                else:
                    self.message_send(peer_id, 'Напишите привет, чтобы получить информацию')

        def finder(self, data: list, offset=None):
    
            if len(self.profiles_list) == 0:
                profiles_list = tools.find_users(data, offset=offset)
                for profile in profiles_list:
                    info_db = extract_from_db(session, profile['id'])
                    if info_db == 1:
                        continue
                    elif info_db == 0:
                        self.profiles_list.append(profile)
            else:
                pass

    def profiles_manager(self, peer_id):
       
        offset = 0
        spl = self.profiles_list
        if len(spl) == 0:
            while len(spl) == 0:
                offset += 30
                print(offset)
                self.finder(self_user_data.getlist, offset=offset)

        elif len(spl) > 0:
            self.sender(peer_id, spl[-1])
            add_to_table(session, profile_id=peer_id, account_id=spl[-1]['id'])
            self.profiles_list.pop()

    def sender(self, peer_id, profile):
       
        photos = tools.find_photos(profile['id'])
        self.message_send(peer_id, f'Ссылка на аккаунт: {profile["name"]}'
                                   f' https://vk.com/id{profile["id"]} '
                                   f'Город {self_user_data.town}')

        for num, photo in enumerate(photos):
            attachment = f'photo{photo["owner_id"]}_{photo["id"]}'
            self.message_send(peer_id, f'Фото номер {num + 1} ', attachment)


if __name__ == '__main__':
    bot_interface = BotInterface(comunity_token, acces_token)
    bot_interface.event_handler()
