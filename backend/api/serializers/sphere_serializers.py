from job.models import Sphere


class SphereSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sphere
        fields = '__all__'