#Parts of speech: vta vti vai vii initial medial final
#                 na ni nad nid adv-pred pc-emph
from django.db import models
class Region(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=10)
class Entry(models.Model)
    lemma = models.ManyToManyField(Word)
    gloss = models.TextField()
    part_of_speech = models.ForeignKey(SubPartOfSpeech)
    stem = models.CharField(max_length = 60)
    header_inflectional_forms = models.ManyToManyField(Phrase)
    audio_for_basic_forms = models.ManyToManyField(Phrase)
    additional_audio = models.ManyToManyField(Phrase)
    relatedwords = models.ForeignKey(RelatedWords)
    reduplication = models.ManyToManyField(Phrase)
    word_parts = models.ManyToManyField(Entry)

class Phrase(models.Model):
    inflection_type = models.CharField(max_length = 20)
    form = models.CharField(max_length= 60)
    audios = models.ManyToManyField(Recording)
class Sentence(models.Model):
    ojibwe = models.TextField()
    english = models.TextField()
    recording = models.ForeignKey(Recording)

class Recording(models.Model):
    audio = models.URLField()
    speaker = models.ForeignKey(Speaker, on_delete=models.PROTECT)

class RelatedWords(models.Model):
    name = models.CharField(max_length=40)
    entries = models.ManyToManyField(Entry)

class WordFamilyEntry(models.Model):
    type = models.CharField(max+length=40)
    entry = models.OneToOneField(Entry)
class WordFamily(models.Model):
    head = models.OneToOneField(Entry)
    entries = models.ManyToManyField(WordFamilyEntry)

class Speaker(models.Model):
    ojibwename = models.CharField(max_length = 60)
    englishname = models.CharField(max_length = 60)
    community = models.CharField(max_length = 60)
    region = models.OneToOneField(Region, on_delete=models.PROTECT)
    initials = models.CharField(max_length=3)
    image = models.URLField()
    statement = models.TextField()
class Culture(models.Model):
    content = models.TextField()
    image = models.URLField()
class PartOfSpeech(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=10)
class SubPartOfSpeech(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=10)
    super_part_of_speech = models.ForeignKey(PartOfSpeech)
class RelatedResources(models.Model):
    content = models.TextField()
    image = models.URLField()
