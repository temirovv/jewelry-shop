from django.db import models


class BTSRegion(models.Model):
    """BTS viloyat/region"""

    bts_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "BTS Viloyat"
        verbose_name_plural = "BTS Viloyatlar"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BTSCity(models.Model):
    """BTS shahar"""

    bts_id = models.IntegerField(unique=True)
    region = models.ForeignKey(BTSRegion, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "BTS Shahar"
        verbose_name_plural = "BTS Shaharlar"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class BTSBranch(models.Model):
    """BTS filial"""

    bts_id = models.IntegerField(unique=True)
    city = models.ForeignKey(BTSCity, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "BTS Filial"
        verbose_name_plural = "BTS Filiallar"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.city.name}"
