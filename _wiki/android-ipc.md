---
layout: wiki
title: 进程间通信
cate1: Android
cate2:
description: 进程间通信
keywords: Android
---

## 进程间通信方式

| 名称            | 优点                                                                                                                 | 缺点                                                                                               | 适用场景                                                           |
|-----------------|----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Intent          | 简单易用                                                                                                             | 只能传输 Bundle 支持的数据类型                                                                     | 四大组件间的进程间通信                                             |
| 文件共享        | 简单易用                                                                                                             | 不适合高并发场景，并且无法做到进程间的即时通信                                                     | 无并发访问，交换简单的数据，实时性不高的场景                       |
| AIDL            | 功能强大，支持一对多并发通信，支持实时通信                                                                           | 使用稍复杂，需要处理好线程同步                                                                     | 一对多通信且有 RPC 需求                                            |
| Messenger       | 功能一般，支持一对多串行通信，支持实时通信                                                                           | 不能很好处理高并发情形，不支持 RPC，数据通过 Message 进行传输，因此只能传输 Bundler 支持的数据类型 | 低并发的一对多即时通信，无 PRC 需求，或者无需要返回结果的 RPC 需求 |
| ContentProvider | 在数据源访问方面功能强大，支持一对多并发数据共享，可通过 ContentProvider 和 ContentResolver 的 Call 方法扩展其它操作 | 可能理解为受约束的 AIDL，主要提供数据源的 CRUD 操作                                                | 一对多的进程间的数据共享                                           |
| Socket          | 功能强大，可以通过网络传输字节流，支持一对多并发实时通信                                                             | 实现细节略繁琐，不支持直接的 RPC                                                                   | 网络数据交换                                                       |

## 参考

* 《Android 开发艺术探索》
