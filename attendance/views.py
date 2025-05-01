from rest_framework import generics
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
