# micropython-gb2312
Display a file encoded by Chinese gb2312 on SSD1306 &amp; rp2040 ( pico like )


## Using ssd1306 to Display a file in gb2312.

配合SSD1306的单色OLED显示屏输出时，发现默认的固件只能显示英文，网上搜了一下大部分都是用现取字模的方式来显示中文。这点感觉不是很方便，就用micropython实现了一下自动根据文件内容解析gb2312点阵字体并展示在ssd1306上。


reference:
  https://github.com/LC044/MCU 
  ssd1306.py
  
font: HZK12 or HZK16   
  
![51a95bb4f5cf4317b4be7eb3c7b9009a](https://user-images.githubusercontent.com/59385989/233077208-0c5da208-4c57-48c7-99cc-e374507fc3d1.jpeg)
