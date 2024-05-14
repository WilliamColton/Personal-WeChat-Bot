from wcferry import Wcf, WxMsg  # 从wcferry库中导入Wcf和WxMsg类
from queue import Empty  # 从queue库中导入Empty异常，用于处理消息队列为空的情况
from threading import Thread  # 从threading库中导入Thread类，用于创建线程

wcf = Wcf()  # 创建Wcf类的实例，用于与微信通信

def processMsg(msg: WxMsg):
    """
    处理微信消息的函数。如果消息来自群聊，打印消息内容。

    参数:
    msg (WxMsg): 接收到的微信消息对象
    """
    if msg.from_group():  # 判断消息是否来自群聊
        print(f"来自群{msg.from_group()}的消息: {msg.content}")  # 打印群聊消息内容

def enableReceivingMsg():
    """
    启用消息接收功能并启动一个新线程来处理接收到的消息。
    """
    def innerWcFerryProcessMsg():
        """
        内部函数，用于在独立线程中循环处理接收到的消息。
        """
        while wcf.is_receiving_msg():  # 判断是否正在接收消息
            try:
                msg = wcf.get_msg()  # 获取接收到的消息
                processMsg(msg)  # 处理消息
            except Empty:  # 处理消息队列为空的情况
                continue  # 继续下一次循环
            except Exception as e:  # 捕获其他所有异常
                print(f"Error: {e}")  # 打印异常信息

    wcf.enable_receiving_msg()  # 启用Wcf实例的消息接收功能
    Thread(target=innerWcFerryProcessMsg, name="ListenMessageThread", daemon=True).start()  # 启动一个后台线程来处理消息

enableReceivingMsg()  # 启用消息接收功能并启动消息处理线程

wcf.keep_running()  # 保持Wcf实例的运行状态，使其持续接收消息




