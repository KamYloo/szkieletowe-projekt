from django.core.exceptions import ValidationError

def validate_file_size(value):
        filesize = value.file.size

        if filesize < 10 * 1024:
            print("za duzy")
            raise ValidationError("The maximum file size that can be uploaded is 10MB")
        else:
            print("dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
            return value