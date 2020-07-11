import PySimpleGUI as sg

class interfaceClass:
    # constructor declare elements
    def __init__ (self):
        self.browse_input = sg.InputText('', size=(70,1), readonly= True, enable_events=True, key='browse_file')
        self.browse_button = sg.FileBrowse('Browse', size=(20,1), target='browse_file')
        self.encap_list_default = sg.Listbox(values=(), size=(36, 10), key = 'encap_list_default')
        self.encap_add = sg.Button('<<', size=(10,2), key='remove_en', pad=(0,0))
        self.encap_remove = sg.Button('>>', size=(10,2), key='add_en', pad=(0,30))
        self.encap_list_add = sg.Listbox(values=(), size=(36, 10), key ='encap_list_add')
        self.remove_list_default = sg.Listbox(values=(), size=(36, 10), key = 'remove_list_default')
        self.remove_add = sg.Submit('<<', size=(10,2), key='remove_remove', pad=(0,0))
        self.remove_remove = sg.Submit('>>', size=(10,2), key='remove_add', pad=(0,30))
        self.remove_list_add = sg.Listbox(values=(), size=(36, 10), key= 'remove_list_add')
        self.progressBar = sg.ProgressBar(100, orientation='h', size=(61, 20), key='progressbar')
        self.passwordLabel = sg.Text('Password')
        self.password_Input = sg.InputText('', key='password', password_char='*', size=(60,1), disabled=True)
        self.process_button = sg.Button('Process', size=(20,1), key='process', disabled=True)

    # layout declaration
    def layout(self):
        encapColumn = [[self.encap_remove], [self.encap_add]]
        removeColumn = [[self.remove_remove], [self.remove_add]]
        return [
                [self.browse_input, self.browse_button],
                [sg.Frame('Encapsulation', 
                    [
                        [self.encap_list_default, sg.Column(encapColumn) , self.encap_list_add]
                    ])],
                [sg.Frame('Remove', 
                    [
                        [self.remove_list_default, sg.Column(removeColumn) , self.remove_list_add],
                    ])],
                [self.progressBar],
                [self.passwordLabel, self.password_Input, self.process_button]
            ]
    
    # load element on window
    def load(self):
        return sg.Window('Data Encapsulation').Layout(self.layout())
    
    # popup message
    def popup(self, message):
        return sg.popup_ok(message)
    
    # tray message
    def tray(self, message):
        sg.SystemTray.notify('Notification', message )

