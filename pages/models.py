from django.db import models

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailsnippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
)
from wagtail.wagtailsearch import index
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from utils.models import LinkFields, ContactFields, RelatedLink, CarouselItem
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailimages.blocks import ImageChooserBlock


class HomePageContentItem(Orderable, LinkFields):
    page = ParentalKey('pages.HomePage', related_name='content_items')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=100)
    content = RichTextField(null=True,blank=True,)
    summary = RichTextField(blank=True)
    slug = models.SlugField()

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('summary'),
        FieldPanel('content'),
        FieldPanel('slug'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]


class HomePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('pages.HomePage', related_name='carousel_items')


class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.HomePage', related_name='related_links')


## MY STREAMFIELD BLOCKS ##

class HtmlBlock(blocks.StructBlock):
    html_content = blocks.TextBlock(required=False)

    class Meta:
        template = 'blocks/html_block.html'
        icon = 'code'

class WysiwygBlock(blocks.StructBlock):
    wysiwyg_content = blocks.RichTextBlock(required=False)
    horizontal_alignment = blocks.ChoiceBlock(choices=[
        ('left', 'Left'),
        ('right', 'Right'),
        ('center', 'Center'),
    ])

    class Meta:
        template = 'blocks/wysiwyg_block.html'
        icon = 'pilcrow'

class ColumnBlock(blocks.StructBlock):
    background_image = ImageChooserBlock(required=False)
    background_color = blocks.TextBlock(required=False)
    padding = blocks.TextBlock(required=False)
    max_width = blocks.TextBlock(required=False)
    content = blocks.StreamBlock([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
    ])

    class Meta:
        template = 'blocks/column_block.html'
        icon = 'grip'

class RowBlock(blocks.StructBlock):
    background_image = ImageChooserBlock(required=False)
    background_color = blocks.TextBlock(required=False)
    padding = blocks.TextBlock(required=False)
    max_width = blocks.TextBlock(required=False)
    vertical_alignment = blocks.ChoiceBlock(choices=[
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('middle', 'Middle'),
        ('baseline', 'Baseline'),
    ])

    content = blocks.StreamBlock([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
        ('Column', ColumnBlock()),
    ])

    class Meta:
        template = 'blocks/row_block.html'
        icon = 'horizontalrule'

class HeroBlock(blocks.StructBlock):
    hero_image = ImageChooserBlock(required=False)
    background_color = blocks.TextBlock(required=False)
    padding = blocks.TextBlock(required=False)
    logo = blocks.ChoiceBlock(choices=[
        ('hide', 'Hide'),
        ('show', 'Show'),
        ('animate', 'Animate'),
    ])
    hero_content = blocks.StreamBlock([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
        ('Row', RowBlock()),
    ])

    class Meta:
        template = 'blocks/hero_block.html'
        icon = 'pick'

class HeroDonateBlock(blocks.StructBlock):
    hero_image = ImageChooserBlock(required=False)
    background_color = blocks.TextBlock(required=False)
    padding = blocks.TextBlock(required=False)
    amount_one = blocks.TextBlock(required=False)
    amount_two = blocks.TextBlock(required=False)
    amount_three = blocks.TextBlock(required=False)
    amount_four = blocks.TextBlock(required=False)
    amount_five = blocks.TextBlock(required=False)
    amount_six = blocks.TextBlock(required=False)
    logo = blocks.ChoiceBlock(choices=[
        ('hide', 'Hide'),
        ('show', 'Show'),
        ('animate', 'Animate'),
    ])
    hero_content = blocks.StreamBlock([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
        ('Row', RowBlock()),
    ])
    thankyou_content = blocks.StreamBlock([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
        ('Row', RowBlock()),
    ])

    class Meta:
        template = 'blocks/hero_donate_block.html'
        icon = 'pick'

class HeroCallToActionBlock(blocks.StructBlock):
    background_color = blocks.TextBlock(required=False)
    pull_up = blocks.TextBlock(required=False)
    cta_content = blocks.StreamBlock([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
        ('Row', RowBlock()),
    ])

    class Meta:
        template = 'blocks/hero_cta_block.html'
        icon = 'pick'

## END OF MY STREAMFIELD BLOCKS ##

class DonatePage(Page):
    title_text = RichTextField(null=True, blank=True)
    feed_image = models.ForeignKey(
        Image,
        help_text="An optional image to represent the page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
        ('Row', RowBlock()),
        ('Hero', HeroDonateBlock()),
        ('Hero_CTA', HeroCallToActionBlock()),
    ],null=True,blank=True)

    class Meta:
        verbose_name = "Donation Page"

DonatePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('title_text', classname="full"),
    StreamFieldPanel('body'),
]



class HomePage(Page):
    title_text = RichTextField(null=True, blank=True)
    feed_image = models.ForeignKey(
        Image,
        help_text="An optional image to represent the page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
        ('Row', RowBlock()),
        ('Hero', HeroBlock()),
        ('Hero_CTA', HeroCallToActionBlock()),
    ],null=True,blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('title_text', classname="full"),
    StreamFieldPanel('body'),
    InlinePanel('carousel_items', label="Carousel items"),
    InlinePanel('content_items', label="Content Blocks"),
    InlinePanel('related_links', label="Related links"),
]

HomePage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]

class StandardIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.StandardIndexPage', related_name='related_links')


class StandardIndexPage(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        Image,
        help_text="An optional image to represent the page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('intro', )

StandardIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('related_links', label="Related links"),
]

StandardIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


# Standard page

class StandardPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('pages.StandardPage', related_name='carousel_items')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('pages.StandardPage', related_name='related_links')


class StandardPage(Page):
    TEMPLATE_CHOICES = [
        ('pages/standard_page.html', 'Default Template'),
        ('pages/standard_page_full.html', 'Standard Page Full'),
    ]
    subtitle = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True)
    body = StreamField([
        ('HTML', HtmlBlock()),
        ('WYSIWYG', WysiwygBlock()),
        ('Row', RowBlock()),
        ('Hero', HeroBlock()),
        ('Hero_CTA', HeroCallToActionBlock()),
    ],null=True,blank=True)
    template_string = models.CharField(
        max_length=255, choices=TEMPLATE_CHOICES,
        default='pages/standard_page.html'
    )
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

    @property
    def template(self):
        return self.template_string


StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full title"),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('body'),
    FieldPanel('template_string'),
    InlinePanel('carousel_items', label="Carousel items"),
    InlinePanel('related_links', label="Related links"),

]

StandardPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]

class ContentBlock(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='contentblocks',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    body = RichTextField()
    summary = RichTextField(blank=True)
    slug = models.SlugField()
    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        FieldPanel('summary'),
        FieldPanel('body', classname="full"),
        FieldPanel('slug'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __unicode__(self):
        return u"{0}[{1}]".format(self.title, self.slug)

register_snippet(ContentBlock)


class Testimonial(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='testimonials',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=150)
    photo = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL
    )
    text = models.CharField(max_length=255)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('name'),
        ImageChooserPanel('photo'),
        FieldPanel('text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __unicode__(self):
        return self.name

register_snippet(Testimonial)


class Advert(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='adverts',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=150, null=True)
    image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL)
    text = RichTextField(blank=True)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('text'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __unicode__(self):
        return self.title

register_snippet(Advert)


# Faqs Page

class FaqsPage(Page):
    body = StreamField([
        ('faq_question', blocks.CharBlock(classname="full title")),
        ('faq_answer', blocks.RichTextBlock()),
    ])

FaqsPage.content_panels = [
    FieldPanel('title', classname="full title"),
    StreamFieldPanel('body'),
]
