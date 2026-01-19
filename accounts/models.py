from django.conf import settings
from django.db import models


class FilmComment(models.Model):
    film_title = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='film_comments',
    )
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        username = self.user.get_username() if self.user else 'guest'
        return f'{self.film_title} – {username}'
