#!/usr/bin/env python
# coding: utf-8

import time
import datetime
import tqdm 
from pynput import mouse,keyboard
from pynput.keyboard import Key

m_keyboard = keyboard.Controller()
m_mouse = mouse.Controller()
default_msg = '***游戏即将开始***'
global game_times,game_delay_microsecond,input_msgs_list #声明 游戏次数与提前时间变量 为全局变量
game_times = 10 #游戏次数
game_delay_microsecond = 30000 #时间判断中的时间提前的微秒数
#pos_num = [i for i in range(game_times)] #
input_msgs_list = ['第{}局'.format(i+1) for i in range(game_times)]  #没局发送的消息
#确定光标操作位置
def mouse_pos_get_click():
    """确定光标操作位置并在光标所在处进行左键点击"""
    print('请在5s内将鼠标移动至发送框')
    time.sleep(5)
    print('当前鼠标位置为：{}'.format(m_mouse.position))
    m_mouse.position = m_mouse.position #重新设置鼠标位置
    mouse_position = m_mouse.position #将属性赋值给变量
    
    m_mouse.click(mouse.Button.left,1) #提前将光标移动至目标位置
    time.sleep(1) #需要间隔
    print('请不要移动光标位置')
    return mouse_position

#直接发自定义信息
def send_single_msg(msg):
    """输入字符串消息并点enter发送"""
    m_keyboard.type(msg)
    time.sleep(0.5)
    m_keyboard.press(Key.enter)
    m_keyboard.release(Key.enter)

    #输入自定义信息
def type_single_msg(msg):
    """仅仅在光标处输入字符串消息
    不发送"""
    m_keyboard.type(msg)
    time.sleep(0.5)
#    m_keyboard.press(Key.enter)
#     m_keyboard.release(Key.enter)

#return datetime类型的所有发送时间的列表
def get_all_send_time():
   """根据当前时间手动确定第一次操作时间，
   并return datetime类型的包含输入时间的
   所有发送时间的列表"""
   now1 = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') #input time
   print("请输入第一次的发送时间,格式如下\n",now1," 即年-月-日-时-分-秒")
   #因后边有time.sleep() 函数，如果当前秒数较小可以选择下一整分钟
   mytime = input("请输入计划的第一次消息发送时间: ")  #调试 判断 时间到达的时间，应设置整分钟，秒数为0
   my_time = mytime + "-000000"
   my_time_y = int(my_time.split('-')[0]) 
   my_time_m = int(my_time.split('-')[1])
   my_time_d = int(my_time.split('-')[2])
   my_time_h = int(my_time.split('-')[3])
   my_time_min = int(my_time.split('-')[4])
   my_time_s = int(my_time.split('-')[5])
   my_time_ms = int(my_time.split('-')[6])
   my_time_int = datetime.datetime(my_time_y,
                                   my_time_m,
                                   my_time_d,
                                   my_time_h,
                                   my_time_min,
                                   my_time_s,
                                   my_time_ms) #转换为datatime 类型时间
   all_send_time = []
   all
   increase_mins = [i for i in range(game_times)]
   for i in range(game_times):  #游戏次数
       every_send_time = my_time_int + datetime.timedelta(minutes=increase_mins[i])
       #根据输入的时间得到游戏次数内所有 等待发送的时间
       print('第{}次游戏计划的发送时间为：{}'.format(i+1,every_send_time))
       every_send_time = every_send_time - datetime.timedelta(microseconds=game_delay_microsecond)
       #上，每次发送的提前一定数值
       all_send_time.append(every_send_time)
   print('\n')
   for i in range(game_times): #打印每次发送的时间
       single_send_time = all_send_time[i]
       single_send_time = single_send_time.strftime('%Y-%m-%d-%H-%M-%S-%f')  
       print('提前{}微秒后,第{}次游戏的时间为: {}'.format(game_delay_microsecond,i+1,single_send_time))
   
   return all_send_time #返回所有时间列表
#     my_time_int = my_time_int - datetime.timedelta(microseconds=40000)
#     all_send_time = [my_time_int + datetime.timedelta(microseconds=1) for  in range(game_times) ]
   
   #上，从输入的字符串时间中得到datatime型时间

#打印剩余时间的进度
def time_left(my_time_int):
    print('第{}调整后的预计发送时间：',my_time_int)
    now_time_process = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')   #process now time 
    print('当前时间为：',now_time_process) 
    now_time_process = datetime.datetime.now()#daterime类型 之间计算 所 差 时间
    left_time = (my_time_int-now_time_process).seconds
    #print(left_time)
    #left_time = int(left_time //0.5) - 2 #提前2秒结束进度报告,这个不是距发送时间的时间，是进度刷新次数
    print('距发送时间还有 ',str(left_time),' s')
    print('\n','='*20,'\n','正在等待到达发送时间\n','='*20)
    print("当前剩余时间约为")
    left_time_list = [str(i+1) for i in range(left_time)] 
    left_time_list.reverse()
    process_time = (left_time - 3)/left_time #剩余时间减去3s 打印一个剩余时间进度后 需要 sleep的时间 
    for i in left_time_list:
        print(i,end = "->")
        time.sleep(process_time)

#循环查看时间,并判断是否点击
def press_enter(my_time_int):
    while True:
        now = datetime.datetime.now() 
        if now > my_time_int:  #与已提前的时间 比较
            m_keyboard.press(Key.enter)  #判断时间与按键后时间 极度一致
            print('\n按enter时间为：',datetime.datetime.now())
            m_keyboard.release(Key.enter)
            print('松开enter时间为：',datetime.datetime.now())
            print('按键时间为：',datetime.datetime.now()) #也不是准确的按键时间，只是请求返回的时间
            #测试了下，多次请求时间，请求需要的时间很短 ，可能是键盘事件需要时间
            print("判断时间为",now)
            #m_keyboard.type(input_msg) #将输入消息单独写成一个函数
            break
def main():
    mouse_position = mouse_pos_get_click() #获取鼠标位置并点击,将鼠标位置赋值给变量
    game_rule = '游戏规则如下：两方按照提示的时间信息，在固定时间发送消息，根据发送消息的快慢判断输赢'
    send_single_msg(game_rule)
    all_send_time_list = get_all_send_time() #得到所有发送 datetime类型 时间的列表
    print('请输入时间后4s内将光标移动至输入框')
    time.sleep(4)
    send_single_msg(default_msg)#发送初始消息
    #the_first_time = all_send_time_list[0].strftime('%时%M分%S秒')
    #the_first_time_msg = '第一局游戏的发送时间为：{},请做好准备'.format(the_first_time)
    #send_single_msg(the_first_time_msg)
    for i in range(game_times): #游戏次数循环
        current_game_time = all_send_time_list[i] + datetime.timedelta(microseconds=game_delay_microsecond)
        current_game_time = current_game_time.strftime('%H时%M分%S秒')  
        current_game_time = '第{}局游戏的发送时间为：{},请做好准备'.format(i+1,current_game_time)
        send_single_msg(current_game_time) #发送 每次游戏的时间
        current_input_msg = input_msgs_list[i] #第 i 次游戏次数 的发送 内容
        type_single_msg(current_input_msg) #输入每局游戏的时间
        current_send_time = all_send_time_list[i] #第i 次 游戏 需要发送的 datetime 时间类型
        print('即将进入第{}局倒计时'.format(i+1))
        time_left(current_send_time) #打印 剩余时间
        press_enter(current_send_time)
        current_game_over_msg = '{}游戏，我已发送消息'.format(current_input_msg) #发送当前局游戏的结束信息
        send_single_msg(current_game_over_msg)

if __name__ == '__main__':
    main()
