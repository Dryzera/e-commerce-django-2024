from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify

class Produto(models.Model):
    
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V', max_length=1, choices=(('V', 'Variação'), ('S', 'Simples'))
    )

    def preco_formatado(self):
        return f'R$ {self.preco_marketing:.2f}.'.replace('.', ',')
    
    def preco_promocional_formatado(self):
        return f'R$ {self.preco_formatado:.2f}.'.replace('.', ',')

    @staticmethod
    def resize_image(img, new_widht=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_wdt, original_hg = img_pil.size

        if original_wdt <= new_widht:
            img_pil.close()
            return

        new_height = round((new_widht * original_hg) / original_wdt)

        new_img = img_pil.resize((new_widht, new_height), Image.LANCZOS)

        new_img.save(img_full_path, optimize=True, quality=50)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.nome, True)
            self.slug = slug

        super().save(*args, **kwargs)

        if self.imagem:
            max_image_size = 600

            self.resize_image(self.imagem, max_image_size)

        

    def __str__(self):
        return self.nome
    
class Variacao(models.Model):

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Variações'
        verbose_name = 'Variação'

    def __str__(self):
        return self.nome or self.produto.nome