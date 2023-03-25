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
