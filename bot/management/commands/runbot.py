from django.core.management import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient, logger
from bot.tg.schemas import Message
from goals.models import Goal, GoalCategory


class TgBotStatus:

    STOK = 0
    CAT_CHOICE = 1
    GOAL_CREATE = 2

    def __init__(self, status_b=STOK, category_id=None):
        self.status_b = status_b
        self.category_id = category_id

    def set_status_b(self, status_b):
        self.status_b = status_b

    def set_category_id(self, category_id):
        self.category_id = category_id

BOT_STATUS = TgBotStatus()

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options):
        offset = 0

        logger.info('Бот готов к работе')
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        if tg_user.user:
            self.handle_authorized_user(tg_user, msg)
        else:
            self.handle_unauthorized_user(tg_user, msg)

    def handle_authorized_user(self, tg_user: TgUser, msg: Message):
        if msg.text == '/goals':
            self.processing_request_goals(tg_user, msg)
        elif msg.text == '/create':
            self.processing_goal_creation(tg_user, msg)
        elif msg.text == '/cancel':
            self.cancellation_processing(msg)
        elif BOT_STATUS.status_b == TgBotStatus.CAT_CHOICE:
            self.checking_selected_category(msg)
        elif BOT_STATUS.status_b == TgBotStatus.GOAL_CREATE:
            self.create_goal(msg, tg_user)
        else:
            self.tg_client.send_message(chat_id=msg.chat.id, text=f'Неизвестная команда {msg.text}')

    def handle_unauthorized_user(self, tg_user: TgUser, msg: Message):
        code = tg_user.generate_verification_code()
        tg_user.verification_code = code
        tg_user.save()

        self.tg_client.send_message(chat_id=msg.chat.id, text=f'Hello! Verification code: {code}')

    def processing_request_goals(self, tg_user: TgUser, msg: Message):
        """все цели участника или владельца доски"""
        qs = (
            Goal.objects.select_related('user')
            .filter(user=tg_user.user, category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
        )

        goals = '\n'.join([f'# {goal.title}' for goal in qs])

        self.tg_client.send_message(chat_id=msg.chat.id, text='No goals' if not goals else goals)

    def processing_goal_creation(self, tg_user: TgUser, msg: Message):
        """категории участника или владельца доски, выбор категории для новой цели"""
        qs = GoalCategory.objects.select_related('user').filter(
            board__participants__user=tg_user.user, is_deleted=False
        )

        categories = '\n'.join([f'-> {cat.title}' for cat in qs])

        if not categories:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Категория не найдена')
        self.tg_client.send_message(chat_id=msg.chat.id, text=f'Выберете категорию \n{categories}')

        BOT_STATUS.set_status_b(TgBotStatus.CAT_CHOICE)

    def checking_selected_category(self, msg: Message):
        """если категория существует, бот предлагает добавить цель"""
        cat = GoalCategory.objects.filter(title=msg.text)
        if cat:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Введите цель')
            BOT_STATUS.set_category_id(category_id=cat[0].id)
            BOT_STATUS.set_status_b(status_b=TgBotStatus.GOAL_CREATE)
        else:
            self.tg_client.send_message(chat_id=msg.chat.id, text=f'Категория "{msg.text}" отсутсвует на доске')

    def create_goal(self, msg, tg_user):
        """Сохраняет цель в категорию"""
        cat = GoalCategory.objects.get(pk=BOT_STATUS.category_id)
        goal = Goal.objects.create(
            title=msg.text,
            category=cat,
            user=tg_user.user,
        )
        self.tg_client.send_message(chat_id=msg.chat.id, text=f'Цель {goal.title} создана')
        BOT_STATUS.set_status_b(TgBotStatus.STOK)

    def cancellation_processing(self, msg: Message):
        """команда для отмены"""
        BOT_STATUS.set_status_b(TgBotStatus.STOK)
        self.tg_client.send_message(chat_id=msg.chat.id, text='Отмена')
