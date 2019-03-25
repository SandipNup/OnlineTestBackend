from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8,required=True)


    def create(self, validated_data):

        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

        # if 'first_name' in validated_data:
        #     user.first_name = validated_data['first_name']

        # if 'last_name' in validated_data:
        #     user.last_name = validated_data['last_name']


        # if 'phone' in validated_data:
        #     user.phone = validated_data['phone']

        # if 'avatar' in validated_data:
        #     user.avatar = validated_data['avatar']


        # user.set_password(validated_data['password'])


        for each in  ['username','password','email']:
                validated_data.pop(each)

        print(validated_data)

        for k, v in validated_data.items():
            setattr(user, k, v)
        user.save()

        return user

    def validate_password(self, value):
        validate_password(value)
        return  value
     

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)
        write_only_fields = ('password',)