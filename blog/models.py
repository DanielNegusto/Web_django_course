from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)  # Заголовок
    content = models.TextField()  # Содержимое
    preview_image = models.ImageField(upload_to='blog_previews/', blank=True, null=True)  # изображение
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)  # Количество просмотров

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
