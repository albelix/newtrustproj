from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from django.core.exceptions import ValidationError

correct_answers = dict(
    cq1_1=30,
    cq1_2=30,
    cq1_3=20,
    cq1_4=31,
    cq1_5=9,
    cq1_6=10,
    cq1_7=10,
    cq1_8=3,
    cq1_9=2,
    cq2_1=0,
    cq2_2=10,
    cq2_3=0,
    cq2_4=10,
    cq2_5=0,
)


class CQ(models.IntegerField):
    def internal_validator(self, value):
        if hasattr(self, 'correct_answer'):
            if value != correct_answers[self.correct_answer]:
                raise ValidationError(f'Please check this answer')

    def __init__(self, *args, **kwargs):
        if 'correct_answer' in kwargs:
            self.correct_answer = kwargs['correct_answer']

        kwargs['validators'] = [self.internal_validator]
        kwargs.pop('correct_answer', None)
        super().__init__(*args, **kwargs)


cq_1_8_choices = ((1, 'Ни для кого'),
                  (2, 'Для 12 – по одному из каждого города, участвующего в исследовании.'),
                  (3, 'Для 1 случайно выбранного участника из одного из 12 городов, участвующих в исследовании.'))
cq_1_9_choices = ((1, '12 – по одному из каждого города, участвующего в исследовании.'),
                  (2, '1 – случайно выбранный участник из одного из 12 городов, принимающих участие в исследовании.  '),
                  (3, 'Ни один не примет')
                  )


class CQPlayer(BasePlayer):
    class Meta:
        abstract = True

    # cqs for part 1
    cq1_1 = CQ(label='Если Участник А передаст свою начальную сумму Участнику Б, сколько токенов получит Участник Б?',
               correct_answer='cq1_1')
    cq1_2 = CQ(
        label='Участник А передал свою начальную сумму Участнику Б. Какую максимальную сумму может Участник Б вернуть обратно Участнику А? ',
        correct_answer='cq1_2')
    cq1_3 = CQ(
        label='Участник Б решает вернуть Участнику А 20 токенов. Сколько токенов получит Участник А от участника Б?',
        correct_answer='cq1_3')
    cq1_4 = CQ(
        label='Сколько токенов получит Участник Б всего за часть 1 эксперимента, если Участник А передаст ему свою начальную сумму, а Участник Б вернет Участнику А 9 токенов?'
        , correct_answer='cq1_4')
    cq1_5 = CQ(
        label='Сколько токенов получит Участник А по итогам эксперимента если он передаст Участнику Б свою начальную сумму, а Участник Б вернет Участнику А 9 токенов?',
        correct_answer='cq1_5')
    cq1_6 = CQ(
        label='Сколько токенов получит Участник А, если он решит не передавать Участнику Б свою начальную сумму? ',
        correct_answer='cq1_6')
    cq1_7 = CQ(
        label='Сколько токенов получит Участник Б, если Участник А решит не передавать Участнику Б свою начальную сумму? ',
        correct_answer='cq1_7')
    cq1_8 = CQ(
        label='Предположим, Вам случайным образом выпала роль Участника А. Для скольких Участников Б Ваше решение о передаче своей начальной суммы будет определяющим для получения его выигрыша?',
        choices=cq_1_8_choices, correct_answer='cq1_8', widget=widgets.RadioSelect)
    cq1_9 = CQ(
        label='Предположим, Вам случайным образом выпала роль Участника Б. Сколько Участников А примут решение о том, получите ли вы их утроенную начальную сумму?',
        choices=cq_1_9_choices, correct_answer='cq1_9', widget=widgets.RadioSelect)

    # cqs for part 1
    cq2_1 = CQ(
        label='В части 1 Участник А из города 1 передал свою начальную сумму Участнику Б. Участника Б из города 1, с которым взаимодействовал этот Участник А, дал оценку что Участник Б из его пары не передаст ему начальную сумму. Сколько токенов получит за эту оценку в части 2 этот Участник Б?',
        correct_answer='cq2_1')
    cq2_2 = CQ(
        label='В части 1 Участник А из города 1 передал свою начальную сумму Участнику Б. Участника Б из города 1, с которым взаимодействовал этот Участник А, дал оценку что Участник Б из его пары передаст ему начальную сумму. Сколько токенов получит за эту оценку в части 2 этот Участник Б?',
        correct_answer='cq2_2')
    cq2_3 = CQ(
        label='В части 1 Участник А из города 1 передал свою начальную сумму Участнику Б из города 2. Участник Б из города 2, с которым взаимодействовал этот Участник А, вернул ему 15 токенов. Участник А в части 2 дал оценку, что этот Участник Б вернул ему 9 токенов. Сколько токенов получит Участник А из этой пары за такую оценку?',
        correct_answer='cq2_3')
    cq2_4 = CQ(
        label='В части 1 Участник А из города 1 не передал свою начальную сумму Участнику Б из города 2. Участник Б из города 2, с которым взаимодействовал этот Участник А, был готов вернуть этому Участнику А 15 токенов в том случае, если бы тот передал ему свою начальную сумму. Участник А в части 2 дал оценку, что этот Участник Б был готов вернуть ему 18 токенов. Сколько токенов получит Участник А из этой пары за такую оценку?',
        correct_answer='cq2_4')
    cq2_5 = CQ(
        label='В части 1 Участник А из города 1 передал свою начальную сумму Участнику Б из города 2. Участник Б из города 2, с которым взаимодействовал этот Участник А, решил ничего не возвращать этому Участнику А в том случае, если бы тот передал ему свою начальную сумму. Участник А в части 2 дал оценку, что этот Участник Б был готов вернуть ему 9 токенов. Сколько токенов получит Участник А из этой пары за такую оценку? ',
        correct_answer='cq2_5')
