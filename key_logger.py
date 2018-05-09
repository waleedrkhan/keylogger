from pynput.keyboard import Key, Listener, Controller
from pynput import mouse
import subprocess as ss

def get_key_status():
    res = ss.Popen(["xset", "-q"], stdout=ss.PIPE)
    out = ss.check_output(('grep','Caps'),stdin=res.stdout).decode('utf-8')
    result = ''.join([i for i in out if not i.isdigit()]).strip('\n').replace(' Lock','_Lock').replace(':','')
    temp = []
    t_list = result.split(' ')
    for one_element in t_list:
        if len(one_element) > 1:
            temp.append(one_element.lower())
    result_dict = dict([(k, v) for k,v in zip (temp[::2], temp[1::2])])
    del temp, t_list, result, res, out
    return result_dict
    

def on_move(x ,y):
    print ("moved to {0}",format((x,y)))

def on_click(x,y,button,pressed):
    if pressed:
        print (button," is pressed at ",x,y)

def on_press(key):
    try:
        print("this is pressed : ",key.char)
    except AttributeError:
        if key.name == 'caps_lock' or key.name == 'num_lock' or key.name == 'scroll_lock':
             value = result_dict[key.name]
             result_dict[key.name] = 'off' if value=='on' else 'on'
             print(key.name, " : ",result_dict[key.name])
        else:
            print("this is pressed : ",key.name)

if __name__ == "__main__":
    result_dict = get_key_status()
    print ("this is final fict : ",result_dict)
    with mouse.Listener(on_move=on_move,on_click=on_click) as listener:
        with Listener(on_press=on_press) as listener:
            listener.join()

