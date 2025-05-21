from django.db.models.signals import pre_save, post_delete, pre_delete
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.dispatch import receiver
from django.conf import settings
from django.db import models
import unicodedata
import random
import string
import os

# Crear una cadena aleatoria de letras y numeros
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_filename_path(filename, setname, sufix, length, lenghtrandom, strpath):
    ext = filename.split('.')[-1]
    texto_normalizado = unicodedata.normalize('NFD', setname)
    setname = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
    setname = setname[:length] if len(setname) > length else setname
    random_string = generate_random_string(lenghtrandom)
    filename = f"{sufix}_{slugify(setname)}_{random_string}.{ext}"
    return os.path.join(strpath, filename)

def set_imgDB_path(instance, filename):
    category = instance.category.category
    instanceTitulo = instance.title.strip().replace(' ', '')
    newName = f'{category}_{instanceTitulo}'
    thispath = os.path.join('imagenes/')
    if instance.category:
        if category == 'Mapa':
            thispath = os.path.join(thispath, 'mapa/')
        elif category == 'Calendario':
            thispath = os.path.join(thispath, 'calendario/')
    return create_filename_path(filename, newName, 'db', 35, 6, thispath)

def set_imgs_path(instance, filename):
    newName = filename.strip().replace(' ', '')
    theName, _  = os.path.splitext(newName)
    thispath = os.path.join('imagenes/')
    return create_filename_path(filename, theName, 'cross_image', 22, 11, thispath)

def set_imgProfile_path(instance, filename):
    newName = instance.user.username.strip().replace(' ', '')
    thispath = os.path.join('imagenes/personal/')
    return create_filename_path(filename, newName, 'profile', 20, 8, thispath)

def set_pdfDB_path(instance, filename):
    newName = instance.title.strip().replace(' ', '')
    thispath = os.path.join('documentos/')
    return create_filename_path(filename, newName, 'db_doc', 18, 10, thispath)


class Categorias(models.Model):
    category = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Database(models.Model):
    uuid = models.CharField(max_length=25, unique=True, default=generate_random_string(25))
    category = models.ForeignKey(Categorias, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    information = models.TextField(blank=True, null=True)
    link_url = models.TextField(blank=True, null=True)
    frecuency = models.IntegerField(default=0)
    document = models.FileField(upload_to=set_pdfDB_path, max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to=set_imgDB_path, max_length=120, blank=True, null=True)
    tags = models.TextField(blank=True, null=True, help_text='Palabras Clave. Separar por comas')
    last_modification = models.DateTimeField(auto_now=True)

    def get_tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        if self.document:
            self.document.delete()
        super(Database, self).delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_info = Database.objects.get(pk=self.pk)
            if old_info.image and old_info.image != self.image:
                old_info.image.delete(save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Base de Datos"
        verbose_name_plural = "Bases de Datos"

class Mapa(models.Model):
    uuid = models.ForeignKey(Database, to_field='uuid', on_delete=models.CASCADE, null=True, blank=True)
    information = models.TextField()
    color = models.CharField(max_length=50)
    coords = models.TextField(blank=True, null=True, help_text='Coordenadas JSON del mapa')
    door = models.CharField(max_length=255, blank=True, null=True, help_text='Coordenadas de la puerta separadas por comas')
    tags = models.TextField(blank=True, null=True, help_text='Palabras Clave. Separar por comas')
    is_marker = models.BooleanField(default=False, help_text='Para los marcadores de imagen')
    hide_name = models.BooleanField(default=False)
    size_marker = models.CharField(max_length=4, default='0.05')
    otheraction = models.TextField(blank=True, null=True, help_text='Acciones adicionales')
    
    def get_tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def __str__(self):
        return self.uuid
    
    class Meta:
        verbose_name = "Mapa"
        verbose_name_plural = "Mapa"

class galeria(models.Model):
    uuid = models.ForeignKey(Mapa, to_field='uuid', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=set_imgs_path, max_length=120, blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.image.name
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super(galeria, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galerias"

class Comments(models.Model):
    name = models.CharField(max_length=150, default='Anónimo')
    email = models.CharField(max_length=200 ,blank=True)
    comments = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=set_imgProfile_path, max_length=120, blank=True, null=True)
    password_update = models.DateField(blank=True, null=True)
    user_token = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_profile = UserProfile.objects.get(pk=self.pk)
            if old_profile.picture and old_profile.picture != self.picture:
                old_profile.picture.delete(save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

# Función genérica para eliminar archivos
def delete_files(instance, fields):
    for field in fields:
        file = getattr(instance, field, None)
        if file:
            file.delete(save=False)

# Señal para eliminar archivos antes de eliminar el objeto
@receiver(pre_delete, sender=Database)
@receiver(pre_delete, sender=galeria)
def delete_files_on_object_delete(sender, instance, **kwargs):
    fields_to_delete = {
        Database: ['image', 'document'],
        galeria: ['image'],
    }
    delete_files(instance, fields_to_delete[sender])


@receiver(post_delete, sender=UserProfile)
def delete_picture_on_delete(sender, instance, **kwargs):
    if instance.picture:
        instance.picture.delete(save=False)
