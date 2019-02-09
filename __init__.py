import os
from cudatext import *
from .io import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_snippet_panel.ini')
fn_icon = os.path.join(os.path.dirname(__file__), 'snip.png')
dir_clips = os.path.join(os.path.dirname(__file__), 'clips')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'


class Command:
    
    def __init__(self):

        self.init_dlg()
        
    def open_dlg(self):

        self.update_combo()
        self.callback_btn_change(0, 0)
        
        title = 'Snippet Panel'
        app_proc(PROC_SIDEPANEL_ADD_DIALOG, (title, self.h_dlg, fn_icon) )
        app_proc(PROC_SIDEPANEL_ACTIVATE, title)
        
    def init_dlg(self):
    
        h=dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={
            #'on_key_down': 'cuda_testing_dlg_proc.callback_tempdlg_on_key_down',
            })
        self.h_dlg = h

        n=dlg_proc(h, DLG_CTL_ADD, 'button_ex')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'btn',
            'align': ALIGN_TOP,
            'act': True,
            'on_change': self.callback_btn_change,
            })
        self.h_btn = dlg_proc(h, DLG_CTL_HANDLE, index=n)
        
        n=dlg_proc(h, DLG_CTL_ADD, 'listbox_ex')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'list',
            'align': ALIGN_CLIENT,
            })
        self.h_list = dlg_proc(h, DLG_CTL_HANDLE, index=n)
        
        button_proc(self.h_btn, BTN_SET_KIND, BTNKIND_TEXT_CHOICE)
        
        listbox_proc(self.h_list, LISTBOX_THEME)
            

    def update_combo(self):
    
        self.clips = sorted(os.listdir(dir_clips))
        button_proc(self.h_btn, BTN_SET_ITEMS, '\n'.join(self.clips))
        button_proc(self.h_btn, BTN_SET_ITEMINDEX, 0)
    
    def update_list(self):
    
        pass

    def get_clips(self, fn):
    
        lines = open_read(fn).splitlines()
        r = []
        for i in lines:
            if '=' not in i:
                r.append((i, i))
            else:
                r.append(i.split('=', maxsplit=2))
        return r
            
        
    def callback_btn_change(self, id_dlg, id_ctl, data='', info=''):

        listbox_proc(self.h_list, LISTBOX_DELETE_ALL)
        id = button_proc(self.h_btn, BTN_GET_ITEMINDEX)
        if id<0: return
        dir = os.path.join(dir_clips, self.clips[id])
        
        l = os.listdir(dir)
        l = [os.path.join(dir, i) for i in l if i.endswith('.txt')]
        if not l: return
        
        items = self.get_clips(l[0])
        for i in items:
            listbox_proc(self.h_list, LISTBOX_ADD, index=-1, text=i[0])
