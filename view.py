import controller
import interface
import time
import os

# ini class constructor
obj = controller.Model()
interfaceObj = interface.interfaceClass()

# load Interface obj
window = interfaceObj.load()

def update_list(element, new_val):
    window.FindElement(element).Update(values=new_val)
    
def checkForHeader(isFileHeader, createFileBase = ''):
    if (isFileHeader):
        response =interfaceObj.popup_yesno(createFileBase + 'Headers detected for all sheet. Proceed with this mode?')
        if (response == 'Yes'):
            user_response = 1
        else:
            user_response = 2
    else:
        response =interfaceObj.popup_yesno(createFileBase + 'No common header found. Proceed with casading mode?')
        if response == 'Yes':
            user_response = 2
        else:
            user_response =1
    if user_response == 1:
        obj.SubsequentHeader()
    else:
        obj.noSubsequentHeader()
 
while True:
    # listen for event emitter and its value        
    event, values = window.Read()  
    progress_bar = window.FindElement('progressbar')

    # window close
    if event in (None, 'Exit'):
        break
    # browse file
    if event == 'browse_file':
        start = time.time()
        obj = controller.Model() # reini obj
        filePath = values["browse_file"]

        # file is selected to proceed
        if len(filePath) > 0 :
            # set and read file
            obj.setFilePath(filePath)
            
            # if file is processed, likely xlsx format
            # return mode type if keyword dictionary is found
            # mode 1 = Encryption Mode, mode 2 = Decryption Mode
            if 'xlsx' in filePath:
                obj.getAttribute()

            # check if merging is necessary
            if obj.mode == 1:
                obj.readDefaultList()
                if 'csv' not in filePath:
                    isFileHeader = obj.detectCommonHeader()
                    checkForHeader(isFileHeader)
            else:
                obj.SubsequentHeader()
                
            # Filter encryption and Remove List 
            obj.readContent()

            # enabling buttons and list on interface
            progress_bar.UpdateBar(0)
            window.FindElement('process').Update(disabled=False)
            window.FindElement('password').Update(disabled=False)
            not_encap = obj.offset(obj.encapsulationList)
            not_remove = obj.offset(obj.removeList)
            update_list('encap_list_default', not_encap)
            update_list('encap_list_add', obj.encapsulationList)
            update_list('remove_list_default', not_remove)
            update_list('remove_list_add', obj.removeList)

            # file meant for decryption process
            if (obj.mode == 2):
                obj.setPassword('') # override default_password
                window.FindElement('remove_en').Update(disabled=True)
                window.FindElement('add_en').Update(disabled=True)
                window.FindElement('remove_remove').Update(disabled=True)
                window.FindElement('remove_add').Update(disabled=True)
                window.FindElement('process').Update('Decrypt')

            # file meant for encryption process
            else:
                window.FindElement('remove_en').Update(disabled=False)
                window.FindElement('add_en').Update(disabled=False)
                window.FindElement('remove_remove').Update(disabled=False)
                window.FindElement('remove_add').Update(disabled=False)
                window.FindElement('process').Update('Encrypt')

            # send notification
            interfaceObj.popup('Data Loaded')

    # listen for remove encrption <<
    elif event == 'remove_en':
        selection = values['encap_list_add']
        # at least being selected
        if len(selection) > 0:
            # update class list and update interface
            obj.encapsulationList.remove(selection[0])
            not_en = obj.offset(obj.encapsulationList)
            update_list('encap_list_default', not_en)
            update_list('encap_list_add', obj.encapsulationList)
    
    # listen for add encryption >>        
    elif event == 'add_en':
        selection = values['encap_list_default']
        # at least being selected
        if len(selection) > 0:
            # cross duplication in removelist
            if selection[0] not in obj.removeList:
                # update class list and update interface
                obj.encapsulationList.append(selection[0])
                not_en = obj.offset(obj.encapsulationList)
                update_list('encap_list_default', not_en)
                update_list('encap_list_add', obj.encapsulationList)
            else:
                # notify of duplication
                interfaceObj.popup("Selected item exist in removed list")

    # listen for remove remove <<
    elif event == 'remove_remove':
        selection = values['remove_list_add']
        # at least one selected
        if len(selection) > 0:
            # update class list and update interface
            obj.removeList.remove(selection[0])
            not_re = obj.offset(obj.removeList)
            update_list('remove_list_default', not_re)
            update_list('remove_list_add',obj.removeList)
            
    # listen for remove add >>
    elif event == 'remove_add':
        selection = values['remove_list_default']
        # at least one selected
        if len(selection) > 0:
            # cross duplication in encrption list
            if selection[0] not in obj.encapsulationList:
                # update class list and interface
                obj.removeList.append(selection[0])
                not_re = obj.offset(obj.removeList)
                update_list('remove_list_default', not_re)
                update_list('remove_list_add', obj.removeList)
            else:
                # notify of duplication
                interfaceObj.popup("Selected item exist in encapsulation list")

    # listen for process button
    elif event == 'process':
        start = time.time()

        # set password if fields is not blank
        if len(values['password'])> 0:
            obj.setPassword(values['password'])

        # encryption mode
        if obj.mode == 1:
            obj.dropColumns()
            obj.encapColumns(progress_bar)
            response = interfaceObj.popup_yesno('Update Keywords?')
            if (response == 'Yes'):
                obj.writeDefaultList()
                
        # decryption mode
        else:
            obj.decapColumns(progress_bar)
        # call write method
        obj.writeFile()
        progress_bar.UpdateBar(100)
        interfaceObj.tray('Done processing! Time taken: %0.2fs ' %  (time.time() - start))


window.Close()

