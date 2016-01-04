from haystack import indexes
from .models import Download
import datetime


class DownloadIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')
    last_modified = indexes.DateTimeField(model_attr='last_modified')

    def get_model(self):
        return Download

    def index_queryset(self, using=None):
        return self.get_model().objects.public_noSort().exclude(product_groups__date_to_publish__gt=datetime.date.today())