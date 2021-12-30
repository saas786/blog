---
layout: post
title: handlerThread
categories: android
description:  handlerThread必知必会
---

{:toc}

[TOC]

### 基础代码

```
private Handler mHandler = new Handler()
	{
		public void handleMessage(android.os.Message msg)
		{
			switch (msg.what)
			{
			case value:
				
				break;
 
			default:
				break;
			}
		};
	};



	//版本1
    Message message = new Message();
    message.what = 0;
    message.obj = "hello";
    mHandler.sendMessage(message); 
    
    ↓
    
    //版本2
    Message message = mHandler.obtainMessage();
    message.what = 0;
    message.obj = "hello";
    mHandler.sendMessage(message);
    
    ↓
    
    //版本3
    mHandler.obtainMessage(0,"hello").sendToTarget();
```

#### 基本逻辑

prepare()创建一个Lopper,

Loppper中包含一个MessageQueue

Handle获取Lopper,进而获取MessageQueue.


#### Handler post

```
mHandler.post(new Runnable()
		{
			@Override
			public void run()
			{
				Log.e("TAG", Thread.currentThread().getName());
				mTxt.setText("yoxi");
			}
		});
```

<b>源码解析:</b>
```
 public final boolean post(Runnable r)
    {
       return  sendMessageDelayed(getPostMessage(r), 0);
    }
  private static Message getPostMessage(Runnable r) {
        Message m = Message.obtain();
        m.callback = r;
        return m;
    }
```
可以看到，在 getPostMessage 中，得到了一个 Message 对象，然后将我们创建的 <font color='red'>Runable 对象作为 callback 属性，赋值给了此 message</font>

handler的post是自产自销其实也是发送了一个消息.只不过这个消息被封装了


### intentService & HandlerThread

#### intentService
service并不会自己创建线程,需要我们自己创建线程.
intentService:给我们自己关闭线程

通常都是在主线程中创建handler然后在子线程中发送数据,
如何在子线程中创建handler来接收数据呢? HandlerThread

#### HandlerThread 

子线程接受主线程的命令.


当前线程指定了Looper对象，不需要使用者显示的调用Looper.prepare()以及Looper.loop()方法


```
class WorkThread extends Thread {
    private Handler mHandler;

    public Handler getHandler() {
        return mHandler;
    }

    public void quit() {
        mHandler.getLooper().quit();
    }

    @Override
    public void run() {
        super.run();
        //创建该线程对应的Looper,
        // 内部实现
        // 1。new Looper（）
        // 2。将1步中的lopper 放在ThreadLocal里，
        // ThreadLocal是保存数据的，主要应用场景是：线程间数据互不影响的情况
        // 3。在1步中的Looper的构造函数中new MessageQueue();
        //其实就是创建了该线程对用的Looper，Looper里创建MessageQueue来实现消息机制
        Looper.prepare();
        mHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);
                Log.d("WorkThread", (Looper.getMainLooper() == Looper.myLooper()) + "," + msg.what);
            }
        };
        //开启消息的死循环处理即：dispatchMessage
        Looper.loop();            //注意这3个的顺序不能颠倒
        Log.d("WorkThread", "end");
    }
    
    public void send(View view) {
        new WorkThread().getHandler().sendEmptyMessage(1);
    }

}
```

#### 如何使用HanlderThread  
可参考IntentService

通过接口实现功能的扩展

```
HandlerThread mHandlerThread = new HandlerThread("WorkThread");
        mHandlerThread.start();
        mHandler = new Handler(mHandlerThread.getLooper()) {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);
                Log.d("WorkThread", (Looper.getMainLooper() == Looper.myLooper()) + "," + msg.what);
            }
        };
```

退出时调用 mHandlerThread.quit()

<b>getThreadHandler不可见</b>




[[android]]