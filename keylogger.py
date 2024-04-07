import os

from collections import defaultdict
from PIL import Image, ImageTk
import time
import json 

import tkinter as tk
from pynput import keyboard

HEIGHT = 350
WIDTH = 550
FONT_FAMILIY = "Consolas"

def apply_keylogger(root, label0,label,label2, button):
    text_file = None
    key_logs = []
    L_LIMIT = 10
    listener = None

    key_press_lookup = defaultdict(bool)

    def update_key_logs(new_event = None):
        if new_event:
            key_logs.append(new_event)

            if len(key_logs) < L_LIMIT:
                return    

        if len(key_logs) == 0:
            return
        
        if os.path.exists('key_log.json'):
            with open('key_log.json', 'r') as file:
                old_key_olgs = json.load(file)
        else:
            old_key_olgs = []
        
        with open('key_log.json', 'w') as file:
            json.dump(old_key_olgs+key_logs, file, indent=2)
 
        key_logs.clear()

    def on_press(key):
        time_stamp = time.time()
        key_str = key.char if hasattr(key, 'char') else str(key)


        if key_press_lookup[key_str]:
            label2.config(text="You aggressively holding,")
            update_key_logs({'held': key_str, 'time': time_stamp})
        else: 
            key_press_lookup[key_str] = True
            label2.config(text="You pressed,")
            update_key_logs({'pressed': key_str, 'time': time_stamp})
        text_file.write(f'{time_stamp}\t{key_str}\n')

        label.config(text=str(key))

    def on_release(key):
        time_stamp = time.time()
        key_str = key.char if hasattr(key, 'char') else str(key)

        key_press_lookup[key_str] = False
        label2.config(text="You released,")
        
        update_key_logs({'released': key_str, 'time': time_stamp})
    
    def start_listening():
        nonlocal listener, text_file
        text_file = open('key_log.txt','a')
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        label0.config(text='Listening to keyboard events...\nLogging the events into\nkey_log.json & key_log.txt')
        button.config(command=stop_listening, text='Stop Keylogger')
        label2.config(text='Type something...')
        label.config(text=':)')
                
    def stop_listening(destroy = False):
        nonlocal text_file, key_logs, key_press_lookup
        if text_file: text_file.close()
        if listener: listener.stop()
        update_key_logs()
        
        if destroy:
            del key_logs, key_press_lookup, text_file
            root.destroy()
        else:
            label0.config(text='Stoped Listening to keyboard events.\nCheck key_log.json & key_log.txt\nfor the logged keyboard events :)')
            button.config(command=start_listening, text='Start Keylogger')

            label2.config(text='Click that button to start it')
            label.config(text='again!!')

        
    button.config(command=start_listening, text='Start Keylogger')
    label2.config(text='Click that button to start the')
    label.config(text='keylogger')
    return lambda : stop_listening(True)


if __name__ == "__main__":
    root = tk.Tk()

    root.title("Keylogger")
    root.resizable(False, False)
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.attributes("-topmost", True)

    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()

    root.geometry("{}x{}+{}+{}".format(WIDTH, HEIGHT, (window_width-WIDTH-int(window_width*.01)), (window_height-HEIGHT-int(window_height*.05))))
   
    background_image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "favbg.png")).resize((WIDTH, HEIGHT))
    background_image = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1) 


    # Info label
    lable0 = tk.Label(root,text=" \n \n ",font=(FONT_FAMILIY, 10),bg="#FFFFFF")
    lable0.pack(side="bottom", pady=10,padx=10, anchor="e")

    # Key Label
    label = tk.Label(root, text=" ",font=(FONT_FAMILIY, 22), width=14,anchor="center", bg="#FFFFFF")
    label.place(x=WIDTH*.41, y=HEIGHT*.11)

    # Event type Label 
    label2 = tk.Label(root, text=' ',font=(FONT_FAMILIY,10), bg="#FFFFFF")
    label2.place(x=WIDTH*.41, y=HEIGHT*.05)

    # Start stop button
    button = tk.Button(root, text=" ",font=(FONT_FAMILIY, 11), bg="#F7EF71")
    button.pack(side="bottom",pady=10,padx=10,anchor="e")

    # Key board listening logic    
    on_close = apply_keylogger(root,lable0,label,label2,button)

    root.protocol("WM_DELETE_WINDOW", on_close)


    try:
        root.mainloop()
    except:
        on_close()


