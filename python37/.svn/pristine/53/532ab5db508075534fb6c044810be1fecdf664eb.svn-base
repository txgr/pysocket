
开始前 url = http://localhost5/api/chat/getRoom
请先检测可用聊天室



##############################################
连接时登录：
发送 json
@room_id  房间id，   房间名称请自行设置
@type  Login
@username  用户名
{"type":"Login", "username":"cx001","room_id":1}

################################################
发言：
{"type":"Say","username":"xxx","to_username":"All","room_id":1,"data_type":"text","content":"我要要要要"}
@to_username = All  群发    else  私聊


################################################
禁言：
{"type":"Banned","username":"xxx","to_username":"dsfe","time":5,"room_id":1,"content":"你骂人了呢"}
@type = Banned
@username 用户名
@to_username 禁谁
@time  单位分钟
@room_id  房间id
@content 原因

成功：
同时返回给设置者和被禁者
{"type":"Banned","username":"xxx","to_username":"dsfe","time":5,"room_id":1,"content":"你骂人了呢"}
失败：
{"type":"Banned","code":66,"msg":"您没有权限~"}
{"code":0,"msg":"没有权限~","time":"1528686369","data":null}

################################################
type =
设置     Set
查看名片 Details
最后发言 Last
屏弊     Shield
关注     Focus


################################################
设置头像：
POST:
http://localhost5/api/Chat/Avatar
@username 用户名
@file 图片单张  jpg,png,bmp,jpeg,gif
enctype="multipart/form-data"
可用cropper.js,Jcrop.js 之类先剪切图片


