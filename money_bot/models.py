from datetime import datetime
from enum import Enum

from tortoise import Model, fields


class OperationType(str, Enum):
    revenue = 'revenue'
    expenditure = 'expenditure'
    any = 'any'

    def ru_name(self):
        return {
            'revenue': 'Доход',
            'expenditure': 'Расход',
            'any': 'Любой',
        }.get(self.value, '')

    @classmethod
    def allowed(cls):
        return [cls.revenue, cls.expenditure]


class TimestampModel(Model):
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)

    class Meta:
        app = 'money_bot'
        abstract = True


class User(TimestampModel):
    full_name: str = fields.CharField(max_length=100)
    username: str = fields.CharField(max_length=100)
    locale: str = fields.CharField(max_length=20)


class Tag(TimestampModel):
    name: str = fields.CharField(max_length=50)
    user: User = fields.ForeignKeyField('money_bot.User', related_name='tags')
    type: OperationType = fields.CharEnumField(OperationType, max_length=20, default=OperationType.any)


class AccountOperation(TimestampModel):
    user: User = fields.ForeignKeyField('money_bot.User', related_name='operations')
    type: OperationType = fields.CharEnumField(OperationType, max_length=20, default=OperationType.expenditure)
    amount: float = fields.FloatField()
    description: str = fields.CharField(max_length=255)
    tags: fields.ManyToManyRelation[Tag] = fields.ManyToManyField('money_bot.Tag', related_name='operations')
