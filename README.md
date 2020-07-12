# Data Anoymonous and Cleaning (DAAC)
*Data Anoymonous and Cleaning (DAAC) is a tool developed in python 3.7.8. Objective of the tool allows the user to removed unecessary 
columns or/and hide sensitive data within the application itself. After that, the processed file could be transferred to other system safely
without revealing sensitive data. To recover the anoymonous data, the file could be feed into the same tool by providing the original secret key*


#
### Features
- [x] Upload and parse any Excel Files into xlsx format
- [x] Predefined encrypted or removed keywords and load into the interface
- [x] Prpgressive progress bar
- [x] Encrypted columns values are reverable with the correct passphrase provided
- [x] Dynamically predefine list by files

#
### Encryption and Decryption
> Uses Fernet Key Cryptography - implementation of symmetric (also known as “secret key”) authenticated cryptography. 
> It takes an average of 71s to complete encrypting 5 columns of 500,000 rows (or 2,500,000 cells)

#
### Software Model
```
view.py (View) -> interface.py (View)
view.py (View) -> controller.py (Model/ Controller) -> Cipher.py
```

#
### Screenshot
![Image of Landing](https://i.ibb.co/hcCQGfz/landing.png)

*Landing page. Everything disabled, other than selecting file browse.*

![Image of listbox population](https://i.ibb.co/dKRjKxX/preload.png)

*Upon excel content loaded, listbox will be populated according to the likeness between default and loaded columns. Now all elements are enabled*

![Image progress bar](https://i.ibb.co/z8GFVWp/encryption.png)

*Progress bar indicator reflected on the interface during encryption/ decryption process*

#
### Usage
```
pip install -r requirements.txt
python view.py
```

#
### Development
- [ ] Support Multiple Page and parse them as singular page
- [ ] Integrated parallelism pandas mechanism. i.e. Dask

