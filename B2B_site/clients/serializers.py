from rest_framework import serializers

"""
Serializes the sitebookdata object to be able to pass it as a JSON.
"""

class SiteBookDataSerializer(serializers.Serializer):
    format=serializers.CharField()
    book_title=serializers.CharField()
    book_img=serializers.CharField()
    book_img_url= serializers.CharField()
    isbn_13=serializers.CharField()
    description=serializers.CharField()
    series=serializers.CharField()
    volume=serializers.CharField()
    subtitle=serializers.CharField()
    authors=serializers.ListField()
    book_id= serializers.CharField()
    site_slug=serializers.CharField()
    parse_status=serializers.CharField()
    url=serializers.CharField()
    content=serializers.CharField()
    ready_for_sale=serializers.CharField()
    score=serializers.CharField()
    extra=serializers.DictField()
