# Bot

这部分内容对应的是bot/bot_interpreter.py

----

#### 公共接口

##### 启动bot commence_life_cycle():
> ```python
> # 启动bot模块，注意不要多次调用
> def commence_life_cycle():
> ```

##### 注册插件 register_plugin(Plugin):

> ```python
> plugin_list = []
> # 将plugin加入到plugin_list,plugin_list将用于消息的分发
> def register_plugin(plugin):
> ```

##### QQMessage

>对QQ消息的封装
> ###### 主要属性:
>> - message: QQ消息的主要文本
>> - sender_number: 发送人QQ号
>> - sender_nickname: 发送人的昵称
>> - 群消息限定:
>>   - group_number: Q群号，没有则为0
>>   - sender_group_card: 发送人的群名片(由于coolQ的某些机制，群名片可能拿不到，此时该属性会被赋值为发送人昵称；另外群名片的更新需要时间)
>###### 主要方法
>> 目前只实现了和nonebot的封装，因此只有一个parse方法
>> ```python
>> # 解析来自nonebot的消息
>> # msg: nonebot中的event
>> def parse_none_bot_message(self, msg):
>> ```

----
#### Plugin接口

##### 消息分发 receive_msg(QQMessage)

> ```python
> available_groups = []
> 
> # 接收到消息时的处理, 基本逻辑如下:
> # plugin相关的(solve_test(), solve(), plugin_description)请看plugin协议
> def receive_msg(message: QQMessage):
> 	# 如果是群消息则判断是否在available_groups
> 	...
>     
> 	# 如果请求手册,则拼接输出每个plugin的手册说明
> 	if message.message in ['帮助', '手册', '说明']:
> 		for plugin in plugin_list:
>       		plugin_description = plugin.solve_description()
> 			# 判断plugin_descriptin中哪些命令可被当前消息响应(如群命令和私聊命令等)
> 			for command in plugin_description.keys():
> 				message.message = command
> 				if plugin.solve_test(message):
> 				... # 拼接消息
>   	# 发送消息
> 	return
> 
>             
> # 判断哪个plugin应该响应本条message,当message被plugin响应后,响应链的判断中止
> for plugin in plugin_list:
> 	if plugin.solve_test(message):
> 		plugin.solve(message)
> 		break
> ```

##### 消息发送 send_msg(QQMessage):

> ```python
> # 调用bot(目前是nonebot)的接口发送消息
> def send_msg(message:QQMessage):
> ```

---

#### Nonebot接口

<del>如果只是开发plugin的话其实不用在意这里</del>

##### 消息监听 message_listener(m):

> 在on_message的时候将消息用QQMessage包装并调用receive_msg()
>
> ```python
> @bot.on_message()
> def message_listener(m):
>    	message = QQMessage()
>    	message.parse_none_bot_message(m)
>    	receive_msg(message)
> ```

##### 消息发送 message_sender(message):

>为了防止消息发送太快,这里利用了一个队列以及一个间隔1秒的定时任务来发送消息
>```python
># 消息队列
>send_queue = []
># 消息添加到发送队列
>def message_sender(message):
>    	...
>	send_queue.append(message)
>    	...
>
># 消息实际发送的位置 间隔1s的定时任务
>@nonebot.scheduler.scheduled_job('interval', seconds=1)
>async def none_bot_send():
>    # 一些对即将发出的消息的处理, 如消息太长需要切分等
>    # 调用nonebot的send_private_message\send_group_msg或其他方法
>```