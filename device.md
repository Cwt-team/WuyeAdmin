下面我将会给你一些接口文档相关的信息。请你核对当前数据库中设备表door_machine_device 是否满足字段要求。如果不满足，直接修改CREATE TABLE 中的字段或类型。下面是第一个：///////////
1.设备心跳包接口
简要描述：

心跳包接口
50秒一次主机设备发往服务器
UDP请求：

地址：www.xxx.com[或者是IP]
端口号:7998
请求方式：

UDP

///发送示例

  {"communityId":"123456","deviceCode":"200111","cmd":"heart",
  "softVer":"1.02.03.04","name":"阳光花园","deviceSn":"asjkdfiouasdjk123"}  

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
cmd	是	string	命令字段，heart是心跳包
softVer	否	string	软件版本号
name	否	string	小区名称
deviceSn	否	string	设备唯一序列号    ///返回示例

  {   "result": "0",   "message": "心跳发送成功" ,"cmd":"heartack"}   返回参数说明

参数名	必选	类型	说明
result	是	String	返回值 0成功 1 失败
message	否	string	描述
cmd	是	string	命令类型 表示心跳包服务返回

2.设备密码校验
简要描述：

密码校验
主机把密码发给服务器校验
请求URL：

https://www.xxx.com/oneLock
www.xxx.com为服务器的域名
请求方式：

POST
参数：

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
onePassword	是	string	密码      //////返回参数说明
返回示例

  {"data":{"unitId":"0021","phone":"13533335555","roomNumber":"0101"},"message":"添加成功","page":null,"code":"0000"}
参数名	必选	类型	说明
data	是	String	返回数据内容
unitId	是	string	楼栋单元号，共4位
phone	是	string	手机号
roomNumber	是	string	用户房号
message	否	string	描述
code	是	string	命令类型 0000成功

3.设备开锁记录
简要描述：

设备开锁之后，主动上报开锁记录给服务器。如果有照片的话，需要填file参数【该参数在开锁照片接口中获取】
请求URL：

http://*******/unlockCallback
请求方式：

POST
参数：

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
type	是	string	开锁类型【0二维码，1小程序远程开锁，2门禁卡，3一次性密码，4人脸，5分机开锁，6物业中心开锁，7指纹开锁，8公共密码开锁,14手机电话开锁】
result	是	string	开锁结果状态 0开锁成功/1无权限 99其他
phone	是	string	手机号,没有号码可填空
roomNumber	是	string	房间号
unitId	是	string	楼栋单元号
file	否	string	开锁照片地址，上传开锁照片服务器返回的地址  /////   返回示例

  {"data":null,"message":"添加成功","page":null,"code":"0000"}
返回参数说明

参数名	必选	类型	说明
data	是	String	返回数据内容
message	否	string	描述
code	是	string	命令类型 0000成功    ///请你核对当前数据库中设备表door_machine_device 是否满足字段要求。如果不满足，直接修改CREATE TABLE 中的字段或类型。


4.设备开锁照片记录
简要描述：

设备开锁之后，主动上报开锁记录给服务器
请求URL：

http://*******/addUpload
请求方式：

POST
multipart/form-data文件流格式上传
示例：

http://******.com/app/equipment/addUpload;uploadFile=/sdcard/1600657724098.jpg;newName=1600657724098.jpg

返回：
{“code”:”0000”,”message”:””,”page”:null,”data”:”/data/page/uploadImages/1600657724098.jpg”}
data：上传开锁照片服务器返回的地址，上传开锁记录时候，需要填此参数，查看记录和照片才能对应

更多返回错误代码请看首页的错误代码描述


5.门口机/录入机下载服务器人脸图片
简要描述：

人脸录入机获取用户人脸照片信息
功能：
1、检测照片是否合格
2、生成特征码供设备使用
请求URL：

http://*******/updateImage
请求方式：

POST
参数：

参数名	必选	类型	说明
communityId	否	string	小区id
deviceCode	否	string	设备编码
timestrap	是	string	时间戳，毫秒为单位
state	否	string	开锁结果状态 0开锁成功/1无权限 99其他
/////请求示例
timestrap=1595582052000
communityId=123485
deviceCode=
请求小区123485，时间戳之后的数据timestrap
参数communityId，deviceCode，state可无参数，也可以值为空

返回示例

  {"data":[{"createTime":1601029003000,"phone":"13694276489","roomNumber":"0102","imageUrl":"\/data\/page\/uploadImages\/16010290032879ca5997b22874631bd9b58ec26f9a8da.JPG",
"state":"10","zipUrl":null,"unitId":"001","communityId":"123500"},{"createTime":1601029003000,"phone":"13694276489","roomNumber":"0101","imageUrl":"\/data\/page\/uploadImages\/16010290032879ca5997b22874631bd9b58ec26f9a8da.JPG","state":"10",
"zipUrl":null,,"unitId":"001","communityId":"123488"}],"id":"消息id",message":"添加成功","page":null,"code":"0000"}
返回参数说明

参数名	必选	类型	说明
data	是	String	返回数据内容
createTime	是	long	记录的时间戳
phone	是	string	记录的手机号
roomNumber	是	string	记录的房号
imageUrl	是	string	记录的图片下载地址
zipUrl |是|string |人脸特征码下载地址，无数据填空 |
|state|是|string |记录的当前状态 10 新增 20 修改 30 删除 40无效图片 50 有效图片 |
|unitId |是|string |记录的楼栋单元号 |
|communityId|是|string |记录的小区id |
|message|否 |string |描述 |
|id|否 |string |消息id，服务器使用 |
|code |是|string |命令类型 0000成功 |



5.门口机/录入机下载服务器人脸图片
简要描述：

人脸录入机获取用户人脸照片信息
功能：
1、检测照片是否合格
2、生成特征码供设备使用
请求URL：

http://*******/updateImage
请求方式：

POST
参数：

参数名	必选	类型	说明
communityId	否	string	小区id
deviceCode	否	string	设备编码
timestrap	是	string	时间戳，毫秒为单位
state	否	string	开锁结果状态 0开锁成功/1无权限 99其他
/////请求示例
timestrap=1595582052000
communityId=123485
deviceCode=
请求小区123485，时间戳之后的数据timestrap
参数communityId，deviceCode，state可无参数，也可以值为空

返回示例

  {"data":[{"createTime":1601029003000,"phone":"13694276489","roomNumber":"0102","imageUrl":"\/data\/page\/uploadImages\/16010290032879ca5997b22874631bd9b58ec26f9a8da.JPG",
"state":"10","zipUrl":null,"unitId":"001","communityId":"123500"},{"createTime":1601029003000,"phone":"13694276489","roomNumber":"0101","imageUrl":"\/data\/page\/uploadImages\/16010290032879ca5997b22874631bd9b58ec26f9a8da.JPG","state":"10",
"zipUrl":null,,"unitId":"001","communityId":"123488"}],"id":"消息id",message":"添加成功","page":null,"code":"0000"}
返回参数说明

参数名	必选	类型	说明
data	是	String	返回数据内容
createTime	是	long	记录的时间戳
phone	是	string	记录的手机号
roomNumber	是	string	记录的房号
imageUrl	是	string	记录的图片下载地址
zipUrl |是|string |人脸特征码下载地址，无数据填空 |
|state|是|string |记录的当前状态 10 新增 20 修改 30 删除 40无效图片 50 有效图片 |
|unitId |是|string |记录的楼栋单元号 |
|communityId|是|string |记录的小区id |
|message|否 |string |描述 |
|id|否 |string |消息id，服务器使用 |
|code |是|string |命令类型 0000成功 |



6.人脸照片检测结果
人脸照片检测结果

简要描述：

人脸照片录入结果
请求URL：
http://*******/authImage
请求方式：

POST
参数：
http://******/authImage?state=50&phone=354756412341&iffile=1

参数名	必选	类型	说明
phone	是	string	用户手机号
state	是	string	记录的当前状态 10 新增 20 修改 30 删除 40无效图片 50 有效图片
file	否	string	multipart/form-data文件流格式，返回人脸特征码
iffile	是	string	2表示无文件，1表示有文件返回
返回示例

  响应方式：
{
code:”0000”,   //0000验证结果成功接收成功  9999验证结果失败
message:””    //提示语
data:{}       
}
返回参数说明

参数名	必选	类型	说明
data	是	String	返回数据内容
communityId	是	string	记录的小区id
message	否	string	描述
code	是	string	命令类型 0000成功

7.服务器触发远程开锁
简要描述：

远程开锁
服务器发给主机的开锁命令
UDP请求：

地址：服务器接收主机心跳包的地址
端口号:服务器接收主机心跳包的端口
请求方式：

UDP

发送示例

  {"communityId":"123456","deviceCode":"200111","cmd":"unlock",
  "phone":"13888889999","roomNumber":"0304","unitId":"0011","id","1"}
参数：

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
cmd	是	string	控制命令
roomNumber	是	string	房号4位长度
unitId	是	string	用户楼栋单元4位长度【0101,010栋1单元】
phone	是	string	手机号，参数必填，可以为””
id	是	string	标识符，服务器用来绑定开锁命令返回命令
返回示例

  {"type": "0","message": "发送成功","deviceCode":"200111" ,"cmd":"unlockack","phone":"13888889999","roomNumber":"0304","id","1"}
返回参数说明

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
type	是	String	返回值 0开门成功 1 参数无效 2无权限
roomNumber	是	string	房号8位长度[3位楼栋1位单元2位楼层2位房间号，00120304位1栋2单元0304房]
message	否	string	描述
cmd	是	string	命令类型 unlockack
id	是	string	标识符，服务器用来绑定开锁命令返回命令


7.服务器触发远程开锁
简要描述：

远程开锁
服务器发给主机的开锁命令
UDP请求：

地址：服务器接收主机心跳包的地址
端口号:服务器接收主机心跳包的端口
请求方式：

UDP

发送示例

  {"communityId":"123456","deviceCode":"200111","cmd":"unlock",
  "phone":"13888889999","roomNumber":"0304","unitId":"0011","id","1"}
参数：

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
cmd	是	string	控制命令
roomNumber	是	string	房号4位长度
unitId	是	string	用户楼栋单元4位长度【0101,010栋1单元】
phone	是	string	手机号，参数必填，可以为””
id	是	string	标识符，服务器用来绑定开锁命令返回命令
返回示例

  {"type": "0","message": "发送成功","deviceCode":"200111" ,"cmd":"unlockack","phone":"13888889999","roomNumber":"0304","id","1"}
返回参数说明

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
type	是	String	返回值 0开门成功 1 参数无效 2无权限
roomNumber	是	string	房号8位长度[3位楼栋1位单元2位楼层2位房间号，00120304位1栋2单元0304房]
message	否	string	描述
cmd	是	string	命令类型 unlockack
id	是	string	标识符，服务器用来绑定开锁命令返回命令

8.服务器触发修改设置
简要描述：

修改设备的配置，根据参数修指定内容[服务器还想修改，添加参数即可，给出需求]
UDP请求：

地址：服务器接收主机心跳包的地址
端口号:服务器接收主机心跳包的端口
请求方式：

UDP

发送示例

  {"communityId":"123456","deviceCode":"200111","cmd":"setting","doorcodeNew","200111","id","1"}
参数：

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
cmd	是	string	控制命令
doorcodeNew	否	string	新的设备编码
communityId	否	string	新的小区编码
id	否	string	标识符，服务器用来绑定命令返回命令
返回示例

  {"type": "0","message": "发送成功","cmd":"settingack","id","1"}
返回参数说明

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
type	是	String	返回值 0成功 1 参数无效 2无权限
id	否	string	标识符，服务器用来绑定命令返回命令


9.服务器触发远程重启
简要描述：

通知设备重启
UDP请求：

地址：服务器接收主机心跳包的地址
端口号:服务器接收主机心跳包的端口
请求方式：

UDP

发送示例

  {"communityId":"123456","deviceCode":"200111","cmd":"reboot","id","1"}
参数：

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
cmd	是	string	控制命令
id	否	string	标识符，服务器用来绑定命令返回命令
返回示例

  {"type": "0","message": "发送成功","cmd":"rebootack","id","1"}
返回参数说明

参数名	必选	类型	说明
communityId	是	string	小区id
deviceCode	是	string	设备编码
type	是	String	返回值 0成功 1 参数无效 2无权限
id	否	string	标识符，服务器用来绑定命令返回命令