import machine
import ssd1306
import framebuf
import time

from utf2gb import utf8_gb2312


i2c = machine.I2C(0, sda=machine.Pin(8), scl=machine.Pin(9), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)



def genword(cw1, ff="HZK16", fpt=16) :
    """ 读取一个汉字
    """
    try:
        f = open(ff,'rb')
    except:
        print("read file ",ff," error!")
    else:
        fsize=fpt*2
        offset = (94*(cw1[0]-0xa0-1)+(cw1[1]-0xa0-1))*fsize;
        f_c1 = f.seek(offset)
        f_c2 = f.read(fsize)
        
        f_c1 = 0
        bmp1=bytearray(f_c2)
        f_c2 = 0
        #print(bmp1)    
        f.close()
        
    key =bytearray(b'\x80\x40\x20\x10\x08\x04\x02\x01')         
  

    for k in range(fpt):
        for j in range(2):
            for i in range(8):
                flag= bmp1[k*2+j] & key[i]
                if flag > 0 :
                    print('●',end='')
                else :
                    #print('○',end='')
                    print(' ',end='')
        print('')

    return bmp1
    
def show_gb2312(cword,fpt,w,h):
    pattern=cword
    fw=16
    if fpt==16:
        fh=16
    else:
        fh=12
        
    buf = framebuf.FrameBuffer(bytearray(pattern), fw, fh, framebuf.MONO_HLSB)
    oled.blit(buf, w, h)
    oled.show()



def clear_gb2312(w,h,fpt=12):
 
    fw=128 
    if fpt==16:
        fh=16
    else:
        fh=12
        
    pattern = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,               
               0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
                
    buf = framebuf.FrameBuffer(bytearray(pattern), fw, fh, framebuf.MONO_HLSB)
    oled.blit(buf, w, h)
    oled.show()


    
if __name__ == '__main__':
    font = utf8_gb2312()
    
    v_width=128-1
    v_height=64-1
    
    f_in = "poem-utf8.txt"
    fpt = 16
    
    v_lines=int(v_height/fpt)
    
    pos_x=0
    pos_y=0
    pos_line=0
                
    try:
        f = open(f_in,'rb')
    except:
        print("read file ",f_in," error!")
    else:
        try:
            while True :
                text_line = f.readline()
                if text_line:
                    tmpr1 = text_line[0:-2]
                    tmpr2=str(tmpr1,'utf-8')
                    
                    pos_line = pos_line + 1
                    pos_x = 0
                    pos_y = (pos_line - 1) * fpt  
                    
                    """ position of current cword in view
                    """
                    pos_c = 0                    
                    
                    if pos_y > v_height - fpt :
                        oled.scroll(0,-(fpt))
                           
                        pos_line = pos_line - 1
                        pos_y = (pos_line -1) * fpt  
                        pos_x=0
                        pos_c=0
                        clear_gb2312(0,pos_y,fpt)                       
                    
                    
                    r=font.str(tmpr2)
                    v1=r

                    if len(v1) == 0 :                                
                        pos_x = 0
                        pos_c = 0
                        clear_gb2312(0,pos_y,fpt)
                        
                    else:
                        time.sleep(1)
                        for i in range(len(v1)/2):                           
                            vy=v1[i*2: i*2+2]
                            if fpt==16:
                                c1=genword(vy,"HZK16",fpt)
                            else:
                                c1=genword(vy,"HZK12",fpt)                
                            print('')
                        
                            
                            show_gb2312(c1,fpt,pos_x,pos_y )
                            #time.sleep(1)
                            pos_c = pos_c + 1
                            pos_x = pos_c * fpt
                            
                            if pos_x > v_width - fpt :
                                pos_x = 0
                                pos_c = 0
                                pos_line = pos_line + 1
                                pos_y = (pos_line - 1) * fpt  
                            
                            if pos_y > v_height - fpt :
                                oled.scroll(0,-(fpt))
                                                                            
                                pos_line = pos_line - 1
                                pos_y = (pos_line -1) * fpt  
                                #pos_x=0
                                #pos_c=0                                
                                clear_gb2312(0,pos_y,fpt)
                                                 
                else:
                    break
            
        finally:
            f.close()
