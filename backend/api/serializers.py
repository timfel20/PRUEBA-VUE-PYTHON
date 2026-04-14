from rest_framework import serializers
from .models import Usuario
from datetime import date

""" The file to validate incoming JSOn before being sent to the database... Checks the format
and every other necessary details """ 
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    
    email = serializers.EmailField(
        error_messages={
            'unique': 'Ya existe un usuario con este correo.',
            'invalid': 'Ingresa un correo válido.'
        }
    )
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'apellidos', 'fecha_nacimiento',
            'ciudad', 'alergias', 'email', 'password',
            'created_at', 'google_sheet_synced'
        ]
        read_only_fields = ['id', 'created_at', 'google_sheet_synced']
    
    def validate_fecha_nacimiento(self, value):
        today = date.today()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )
        if age < 13:
            raise serializers.ValidationError(
                "Debes tener al menos 13 años para registrarte."
            )
        return value
    
    def validate_alergias(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Las alergias deben ser una lista."
            )
        return value
    
    def validate_ciudad(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("La ciudad es obligatoria.")
        return value.strip().title()
    
    def create(self, validated_data):
        return Usuario.objects.create(**validated_data)