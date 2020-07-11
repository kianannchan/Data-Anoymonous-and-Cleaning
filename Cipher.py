import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class cipherClass:
    def __init__(self):
        self.key = ''
        
    def setKey(self, password):
        password = password.encode() 
        salt = b'SQLShack_' 
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1,
            backend=default_backend()
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(password)) 
            
    def encrypt(self, plainText):
        try:
            f = Fernet(self.key)
            return f.encrypt(plainText.encode()).decode()
        except Exception as e:
           print(e)
    
    def decrypt(self, cipherText):
        try:
            f = Fernet(self.key)
            return f.decrypt(cipherText.encode()).decode()
        except Exception as e:
            print(e)




