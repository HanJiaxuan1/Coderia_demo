from haystack import indexes

from .models import Note


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    create_time = indexes.DateTimeField(model_attr='create_time')
    importance = indexes.DateTimeField(model_attr='importance')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        result_set = self.get_model().objects.order_by('-create_time')
        return result_set
