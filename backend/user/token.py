from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from user.models import User, PasswordResetOTP

tok = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY4MTUxMzcyLCJpYXQiOjE3NjgxNDk1NzIsImp0aSI6IjMzY2E4MjY1ZmZhZjQxZDM4OWYxZTJmMDA5OWM1MTFiIiwidXNlcl9pZCI6IjE2IiwicHVycG9zZSI6InBhc3N3b3JkX3Jlc2V0In0.n7G4dTEJmyxwnmL01GxEu9I2UF5zXcl7o5BlcVBBfDc"


# 1. can SimpleJWT parse it?
try:
    at = AccessToken(tok)
    print("parsed ok")
    print("claims:", {k: at[k] for k in at.keys()})
except TokenError as e:
    print("TokenError:", str(e))
    raise

# 2. check user exists
user_id = at.get('user_id') or at.get('user') or at.get('user_id')
print("user_id in token:", user_id)
print("user exists:", User.objects.filter(pk=int(user_id)).exists())

# 3. check stored OTP row matches token string exactly
print("token length:", len(tok))
print("otp rows matching token:", list(PasswordResetOTP.objects.filter(reset_token=tok).values('id','user_id','is_verified','is_used') ))
