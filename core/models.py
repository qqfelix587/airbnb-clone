from django.db import models


class TimeStampedModel(models.Model):
    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    # auto_now_add : Model이 생성될 시 날짜를 추가
    updated = models.DateTimeField(auto_now=True)
    # auto_now : Model이 update될때마다 날짜를 수정

    class Meta:
        abstract = True
        # abstract Model : DB에 나타나지 않는 모델
        # 해당 과정에서 time stamped model은 다른 모델에 inherit 해주기 위해 쓰이는 것이므로...
