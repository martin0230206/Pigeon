
from tortoise import fields, models


class Test(models.Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    datetime = fields.DatetimeField(null=True)

    class Meta:
        table = "test`.`test"

    def __str__(self):
        return self.name
