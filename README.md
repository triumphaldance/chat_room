## 题目要求

> 设计和实现一个聊天系统,它允许多组用户进行聊天活动。有一个聊天协调器位于某一个知名的网络地址上,它使用UDP与聊天客户通信,并且为每个聊天会话建立聊天服务器,而且维护一个聊天会话目录。每个聊天会话都有一个聊天服务器。聊天服务器使用TCP与聊天客户通信。聊天客户允许用户启动、加人或者离开一个聊天会话。请设计和实现协调器、服务器和客户的代码。



## 代码部分

### client.py（客户端）

### coordinator.py（聊天协调器）

### serve.py（聊天服务器）



## 代码分析

### 1. 客户端 (`Client`)

#### 主要功能：
- 发送和接收消息。
- 连接到协调器请求创建或加入聊天会话。
- 连接到具体的聊天服务器进行聊天。

#### 工作流程：
1. **初始化**：创建UDP和TCP套接字。
2. **发送消息**：通过UDP套接字发送消息到协调器，并处理响应。
3. **创建或加入会话**：
   - 创建：发送“CREATE”消息到协调器。
   - 加入：发送“JOIN session_id”消息到协调器。
4. **连接服务器**：根据协调器的响应，连接到指定的聊天服务器。
5. **聊天**：通过TCP套接字发送和接收消息。
6. **接收消息**：在单独的线程中不断接收并打印服务器发送的消息。
7. **关闭连接**：退出时关闭TCP连接。

### 2. 协调器 (`Coordinator`)

#### 主要功能：
- 处理客户端的会话创建和加入请求。
- 启动和管理多个聊天服务器实例。

#### 工作流程：
1. **初始化**：创建UDP套接字并绑定到指定地址和端口。
2. **监听**：在无限循环中接收客户端消息。
3. **处理请求**：
   - 创建会话：分配新的会话ID，启动新的聊天服务器，并返回会话信息给客户端。
   - 加入会话：检查会话ID是否存在，存在则返回会话信息给客户端，否则返回“SESSION NOT FOUND”。
4. **启动服务器**：每个新会话启动一个新的聊天服务器实例，并在单独的线程中运行。

### 3. 聊天服务器 (`Server`)

#### 主要功能：
- 处理多个客户端的连接和消息。
- 广播消息给所有连接的客户端。

#### 工作流程：
1. **初始化**：创建TCP套接字并绑定到指定地址和端口。
2. **运行**：在无限循环中接受客户端连接。
3. **处理客户端**：
   - 每个新连接创建一个新线程处理该客户端的消息。
   - 接收客户端消息并进行广播。
   - 处理用户退出，将其从客户端列表中移除。
4. **广播消息**：将消息发送给所有其他客户端。

### 总体运行逻辑：

1. **客户端请求会话**：
   - 用户启动客户端，并通过输入命令请求创建或加入会话。
   - 客户端通过UDP套接字发送请求到协调器。

2. **协调器处理请求**：
   - 协调器接收请求并根据请求类型创建新会话或查找已有会话。
   - 若创建新会话，协调器启动一个新的聊天服务器实例，并返回会话信息给客户端。
   - 若加入会话，协调器返回会话的服务器信息给客户端。

3. **客户端连接服务器**：
   - 客户端根据协调器的响应，通过TCP套接字连接到指定的聊天服务器。
   - 客户端在连接后可以发送和接收消息。

4. **聊天服务器处理消息**：
   - 服务器接受客户端连接，并为每个客户端启动一个新线程处理消息。
   - 服务器接收客户端的消息并广播给所有其他客户端。

客户端、协调器和聊天服务器共同协作，构成了一个完整的聊天室系统。协调器负责会话的管理和分发，聊天服务器负责消息的转发和处理，客户端通过协调器连接到服务器进行聊天。

## 运行结果

> 客户端多开：6个

![image-20240514230425745](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514230425745.png)

> 聊天协调器：开启

![image-20240514230627481](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514230627481.png)

> 命令：
>
> start：开启一个聊天群
>
> join：加入现存聊天群
>
> send：发送消息
>
> exit：退出群聊

### 创建/加入群聊

#### client1（创建群聊1）

![image-20240514230858362](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514230858362.png)

#### client2（加入群聊1）

![image-20240514230906460](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514230906460.png)

#### client3（加入群聊1）

![image-20240514231013291](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231013291.png)

#### client4（加入群聊1）

![image-20240514231021548](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231021548.png)

#### 调解器message

![image-20240514231330734](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231330734.png)





#### client5（创建群聊2）

![image-20240514231148572](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231148572.png)

#### client6（加入群聊2）

![image-20240514231138055](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231138055.png)

#### 调解器message

![image-20240514231405008](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231405008.png)

---

### 发送消息

#### client1

![image-20240514231704496](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231704496.png)

#### client2（加入群聊1）

![image-20240514231715964](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231715964.png)

#### client3（加入群聊1）

![image-20240514231731857](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231731857.png)

#### client4（加入群聊1）

![image-20240514231751664](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231751664.png)

#### 调解器message

![image-20240514231814506](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231814506.png)

#### client5（创建群聊2）

![image-20240514231913465](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231913465.png)

#### client6（加入群聊2）

![image-20240514231925384](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231925384.png)

#### 调解器message



![image-20240514231948056](C:\Users\wyc73\AppData\Roaming\Typora\typora-user-images\image-20240514231948056.png)