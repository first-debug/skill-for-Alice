from django.db import models


class Heroes(models.Model):
    name = models.CharField( max_length=19)
    primary_attr = models.CharField( max_length=3)
    attack_type = models.CharField( max_length=6)
    start_damage = models.CharField( max_length=5)
    start_health = models.IntegerField()
    start_health_regen = models.FloatField()
    start_mana = models.IntegerField()
    start_mana_regen = models.FloatField()
    start_armor = models.IntegerField()
    start_attack_speed = models.IntegerField()
    start_mr = models.IntegerField()
    base_str = models.IntegerField()
    base_agi = models.IntegerField()
    base_int = models.IntegerField()
    str_gain = models.FloatField()
    agi_gain = models.FloatField()
    int_gain = models.FloatField()
    possible_name = models.CharField(max_length=200)
    image_id = models.TextField(default='')


class Items(models.Model):
    name = models.CharField(max_length=32)


class Answer(models.Model):
    type_ans = models.CharField(max_length=10)
    text = models.CharField(max_length=1024)


class UserData(models.Model):
    user_id = models.TextField(primary_key=True)
    count_unrec = models.IntegerField(default=0)
    recent_names = models.TextField(default='')


class NewPossibleNames(models.Model):
    name = models.CharField( max_length=19)
    possible_name = models.CharField(max_length=200)
