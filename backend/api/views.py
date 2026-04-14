from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import IntegrityError

from .models import Usuario
from .serializers import UsuarioSerializer
from .services.google_sheets import get_sheets_service


@api_view(['POST'])
@permission_classes([AllowAny])
def registro_usuario(request):
    """ Endpoint para registrar un nuevo usuario. 
    URL: POST /api/registro/ """
    serializer = UsuarioSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {
                'success': False,
                'message': 'Error de validación',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        usuario = serializer.save()
    except IntegrityError:
        return Response(
            {
                'success': False,
                'message': 'El email ya está registrado'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    sheets_synced = False
    try:
        service = get_sheets_service()
        sheets_synced = service.append_user(usuario)
        if sheets_synced:
            usuario.google_sheet_synced = True
            usuario.save(update_fields=['google_sheet_synced'])
    except Exception as e:
        print(f"Error syncing to Google Sheets: {e}")
    
    return Response(
        {
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellidos': usuario.apellidos,
                'email': usuario.email,
                'ciudad': usuario.ciudad,
                'created_at': usuario.created_at,
            },
            'sheets_synced': sheets_synced
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'ok', 'message': 'API is running'})