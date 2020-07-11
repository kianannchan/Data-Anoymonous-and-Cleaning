# Data Anoymonous and Cleaning (DAAC)
*Data Anoymonous and Cleaning (DAAC) is a tool developed in python 3.7.8. Objective of the tool allows the user to removed unecessay 
columns or hide sensitive data within the application itself*


#
### Features
- [x] Upload and parse any Excel Files into xlsx format
- [x] Predefined encrypted or removed keywords and load into the interface
- [x] Prpgressive progress bar
- [x] Encrypted columns values are reverable with the correct passphrase provided


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
### Development
- [ ] Support Multiple Page and parse them as singular page
- [ ] Dynamically predefine list by files

