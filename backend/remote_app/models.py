from django.db import models
from django.template.defaultfilters import slugify  # new
import os
import uuid


def upload_app_zip(instance, filename, **kwargs):
    return "/".join(["app_zip", str(instance.guid), f"{instance.name}.zip"])


class RemoteApp(models.Model):

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    app_zip = models.FileField()

    def __str__(self) -> str:
        return f"{self.name} - ({self.guid})" 

    class Meta:
        verbose_name = "Программное обеспечение на сервере"
        verbose_name_plural = "Программное обеспечение на сервере"
        ordering = ["-date_created"]

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class RemoteAppFileConfigType(models.Model):

    remote_app = models.ForeignKey(RemoteApp, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, null=False)
    is_required = models.BooleanField(default=True)
    file_path = models.FilePathField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Тип конфигурации программного обеспечения на сервере"
        verbose_name_plural = "Типы конфигураций программного обеспечения ПО на сервере"
        ordering = ["pk"]


class RemoteAppTask(models.Model):

    class TaskStatus(models.IntegerChoices):
        NOT_STARTED = 1 # Еще не запускалась
        PENDING = 2     # В очереди на запуск
        PROCESSING = 3  # Запущена и обрабатывается
        SUCCESS = 4     # Успешно выполнена
        ERROR = 5       # Ошибка выполнения

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    remote_app = models.ForeignKey(RemoteApp, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED
    )
    status_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Задача исполнения программного обеспечения"
        verbose_name_plural = "Задачи исполнения программного обеспечения"
        ordering = ["-date_created"]


def config_file_upload(instance, filename, **kwargs):
    return "/".join(["config_files", str(instance.guid), filename])


class RemoteAppTaskFileConfig(models.Model):

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    config_type = models.ForeignKey(RemoteAppFileConfigType, on_delete=models.CASCADE)
    config_file = models.FileField(upload_to=config_file_upload, blank=True, null=True)
    remote_app_task = models.ForeignKey(RemoteAppTask, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Конфигурация экземпляра запуска программного обеспечения"
        verbose_name_plural = "Конфигурации экземпляров запуска программного обеспечения"

    def config_filename(self):
        if self.config_file:
            return os.path.basename(self.config_file.name) 
        return ''

