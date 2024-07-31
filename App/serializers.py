from rest_framework import serializers  
from .models import CadastroViabilidade

class ListVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastroViabilidade
        fields = '__all__'