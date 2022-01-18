from django.db import models


class TimeStampedModel(models.Model):
    """Time Stamped Model"""

    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        abstarct: True
        # abstract Model : DB에 나타나지 않는 모델
        # 해당 과정에서 time stamped model은 다른 모델에 inherit 해주기 위해 쓰이는 것이므로...
