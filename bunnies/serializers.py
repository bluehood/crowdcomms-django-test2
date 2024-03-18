from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.response import Response

from bunnies.models import Bunny, RabbitHole

class BunnySerializer(serializers.ModelSerializer):

    home = serializers.SlugRelatedField(queryset=RabbitHole.objects.all(), slug_field='location')
    family_members = serializers.SerializerMethodField()

    def get_family_members(self, obj):
        return []

    class Meta:
        model = Bunny
        fields = ('name', 'home', 'family_members')

    def validate(self, attrs):
        print(Bunny.objects.filter(home=attrs).count(), attrs.bunnies_limit)
        if Bunny.objects.filter(home=attrs).count() >= attrs.bunnies_limit:
            return serializers.ValidationError('No more bunnies can fit in the rabbithole')

        return attrs

class RabbitHoleSerializer(serializers.ModelSerializer):

    bunnies = serializers.PrimaryKeyRelatedField(many=True, queryset=Bunny.objects.all())
    bunny_count = serializers.SerializerMethodField()

    # bunnies = BunnySerializer(many=True, read_only=True)
    # bunny_count = serializers.SerializerMethodField()

    def get_bunny_count(self, obj):
        # Return the number of bunnies
        return obj.bunnies.count()

    class Meta:
        model = RabbitHole
        fields = ('location', 'bunnies', 'bunny_count', 'owner')



