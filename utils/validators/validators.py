import os
from rest_framework import serializers

def validate_image(value, max_size_mb=2, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    max_size = max_size_mb * 1024 * 1024  # MB to bytes

    # Check content type
    if not value.content_type.startswith('image/'):
        raise serializers.ValidationError("Only image files are allowed.")

    # Check size
    if value.size > max_size:
        raise serializers.ValidationError(f"Image size must be less than {max_size_mb}MB.")

    # Check extension
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise serializers.ValidationError(
            f"Unsupported file extension '{ext}'. Allowed: {', '.join(allowed_extensions)}."
        )

    return value