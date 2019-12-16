from django.db import models


class Post(models.Model):
    title = models.CharField('タイトル', max_length=255)
    created_at = models.DateTimeField('作成日', auto_now_add=True)

    def __str__(self):
        # インタラクティブシェルで見やすいようにしています。
        return f'pk:{self.pk} title:{self.title} created_at:{self.created_at}'
