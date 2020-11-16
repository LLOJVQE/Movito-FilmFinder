from django.db import models
from urllib import request
import ssl

# Create your models here.

# Movie genres tag
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='genres_name')

    class Meta:
        indexes = [
            models.Index(fields=['id', 'name']),
            models.Index(fields=['id'], name='genres_id_idx'),
        ]
        verbose_name = 'Genre'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Director(models.Model):

    id = models.TextField(verbose_name="director_id",primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Name')

    class Meta:
        indexes = [
            models.Index(fields=['id', 'name']),
            models.Index(fields=['id'], name='id_idx'),
        ]
        verbose_name = 'director'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    movie info
    """
    id = models.TextField(verbose_name="IMDBID",primary_key=True)

    # id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='Title', max_length=200,default='')
    director = models.TextField(verbose_name="Director", default='',blank=True,null=True)
    directors = models.ManyToManyField('Director',related_name='director_movie')
    cast = models.TextField(verbose_name="Cast", default='',blank=True,null=True)
    # tag= models.ForeignKey(Tag, default='', on_delete=models.DO_NOTHING, verbose_name='类型标签')
    genres = models.ManyToManyField('Tag')
    genres_text = models.TextField(verbose_name="genres in text", default='',blank=True,null=True)
    info = models.TextField(verbose_name="Info", default='',blank=True,null=True)
    year = models.CharField('Year', max_length=10, blank=True, null=True)
    run_time = models.CharField('Run Time', max_length=10, blank=True, null=True)
    logo = models.ImageField(upload_to='banner/%Y/%m', default='image/default.png',blank=True,null=True, max_length=100, verbose_name='封面')
    star = models.FloatField(verbose_name='Rate',default=0)
    star_personal = models.FloatField(verbose_name='Rate_from_whitelist', default=0)
    comment_nums = models.IntegerField(verbose_name='Comment numbers',default=0)
    img_path = models.TextField(verbose_name="image path", default='',blank=True)

    # add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    # def image_data(self):
    #     head = {}
    #
    #     context = ssl._create_unverified_context()
    #
    #     head['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15'
    #     # 创建Request对象并添加heads
    #     req = request.Request('https://api.themoviedb.org/3/find/'
    #                           +self.id+'?api_key=1a0eeda873912b473a595640ef04b25e&language=en-US&external_source=imdb_id', headers=head)
    #     # 传入创建好的Request对象
    #     response = request.urlopen(req,context=context)
    #     # 读取响应信息并解码
    #     html = response.read().decode('utf-8')
    #     img_url = html.split('"poster_path":"')[1].split('"')[0]
    #     # 打印爬到的信息
    #     return 'https://image.tmdb.org/t/p/w500/' + img_url
    # def image_url(self):
    #
    #     # img_addr = format_html('https://api.themoviedb.org/3/find/{}?api_key=1a0eeda873912b473a595640ef04b25e&language=en-US&external_source=imdb_id',self.imdb)
    #
    #     return 'https://image.tmdb.org/t/p/w500/' + '2pwwawlnti0BoluxFiksnVg5TZ7.jpg'
    def __str__(self):
        return self.title  # 主要__str__最好是个字符串，不然你会遇到很多的坑，还有我们返回的这两个字段填写数据的时候必须写上数据，必然相加会报错，null类型和str类型不能相加等错误信息。

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = verbose_name





