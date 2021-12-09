from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField


class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)

        context['products'] = Product.objects.child_of(self).live()

        return context


class Product(Page):
    def get_context(self, request):
        context = super().get_context(request)
        fields = []
        for f in self.custom_fields.get_object_list():
            if f.options:
                f.options_array = f.options.split('|')
                fields.append(f)
            else:
                fields.append(f)

        context['custom_fields'] = fields

        return context
    sku = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    body = RichTextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    content_panels = Page.content_panels + [
        FieldPanel('sku'),
        FieldPanel('price'),
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel('short_description'),
        FieldPanel('body', classname="full"),
        InlinePanel('custom_fields', label='Custom fields'),
    ]


class ProductGalleryImage(Orderable):
    page = ParentalKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class ProductCustomField(Orderable):
    product = ParentalKey(Product, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('options')
    ]
