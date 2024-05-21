from django.db import models
from product.models import Product
from django.conf import settings

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to your main model
    image = models.ImageField(upload_to='thumbnail')  # Path to store images
    caption = models.CharField(max_length=255, blank=True)  # Optional caption field

    def get_image_url(self):
            if self.image:
                # url=self.thumbnail.url.split('/')
                # url=url[-1]
                # BASE_DIR = Path(__file__).resolve().parent.parent
                # thumbnail_root = os.path.join(BASE_DIR, 'thumbnail')
                # image_url = f'{thumbnail_root+'\\'+url}' 
                # image_url=image_url.replace("\\","/")
                
                return settings.API_DOMAIN+'/'+self.image.url  # Return the image URL
            else:
                return None  # Handle cases where no image is uploaded