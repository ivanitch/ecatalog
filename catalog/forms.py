from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product

FORBIDDEN_WORDS = [
    'казино',
    'биржа',
    'обман',
    'криптовалюта',
    'дешево',
    'полиция',
    'крипта',
    'бесплатно',
    'радар',
]

MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = ('image/jpeg', 'image/png')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        if 'description' in self.fields:
            self.fields['description'].widget.attrs['rows'] = 10

    @staticmethod
    def _check_forbidden_words(value):
        lowered = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise ValidationError(f'Использование слова "{word}" запрещено.')
        return value

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return self._check_forbidden_words(name)

    def clean_description(self):
        description = self.cleaned_data.get('description') or ''
        if description:
            self._check_forbidden_words(description)
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            content_type = getattr(image, 'content_type', None)
            if content_type and content_type not in ALLOWED_IMAGE_TYPES:
                raise ValidationError('Изображение должно быть в формате JPEG или PNG.')
            if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
                raise ValidationError(f'Размер изображения не должен превышать {MAX_IMAGE_SIZE_MB} МБ.')
        return image
