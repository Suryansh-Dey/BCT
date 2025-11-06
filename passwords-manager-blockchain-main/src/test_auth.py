import pyotp, time
secret ="JDB4KW6GTBQ6RJBWZGXR5ORTDZ2JE4LU"
totp = pyotp.TOTP(secret)
print("Current code:", totp.now())
print("Time remaining in this 30s window:", 30 - int(time.time()) % 30, "seconds")