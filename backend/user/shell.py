
# python manage.py shell
from user.models import User

u = User.objects.get(email="kaushalshinde18@gmail.com")
u.telegram_chat_id = "1321713645"

u.save()



# curl -X POST http://127.0.0.1:8000/user/ \
#   -H "Content-Type: application/json" \
#   -d '{
#     "name": "Kaushal",
#     "email": "kaushalshinde18@gmail.com.com",
#     "phone": "986-173073",
#     "password": "kaushal",
#     "type": "user",
#     "telegram_chat_id": "1321713645"
#   }'
