from django import template

register = template.Library()


@register.filter('show_audio_video_attrs')
def get_audio_video_attrs(value):
    return ', '.join([attr for attr in value if attr in '2d 3d subbed dubbed imax screenx 4dx'])

