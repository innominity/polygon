from django.db import models
from django.template.defaultfilters import slugify  # new
import uuid


class RemoteApp(models.Model):

    name = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Удаленное ПО на сервере"
        verbose_name_plural = "Удаленные ПО на сервере"
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

    class Meta:
        verbose_name = "Тип конфигурации удаленного ПО на сервере"
        verbose_name_plural = "Типы конфигураций удаленного ПО на сервере"
        ordering = ["pk"]


class RemoteAppTask(models.Model):

    class TaskStatus(models.IntegerChoices):
        PENDING = 1
        STARTED = 2
        RUNNING = 3
        SUCCESS = 4
        ERROR = 5

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    remote_app = models.ForeignKey(RemoteApp, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED
    )
    status_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Задача исполнения удаленного ПО"
        verbose_name_plural = "Задачи исполнения удаленного ПО"
        ordering = ["-date_created"]


def config_file_upload(instance, filename, **kwargs):
    return "/".join(["config_files", str(instance.guid), "orig", filename])


class RemoteAppTaskFileConfig(models.Model):

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    config_type = models.ForeignKey(RemoteAppFileConfigType, on_delete=models.CASCADE)
    config_file = models.FileField(upload_to=config_file_upload, blank=True, null=True)


    class Meta:
        verbose_name = "Конфигурация экземпляра запуска удаленного ПО"
        verbose_name_plural = "Конфигурации экземпляров запуска удаленного ПО"