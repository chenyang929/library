## 图书借阅管理系统

### 功能说明
- 前台
    + 用户使用邮箱和初始密码登录，登录后可修改初始密码
    + 登录后可以借阅和归还图书
    + 设置每个用户最多借阅两本图书
    + 借阅和归还图书均需管理员审批
- 后台
    + 管理员使用专用邮箱和密码登录
    + 可以审批用户借阅和归还图书
    + 可以新增和修改图书信息
    + 可以新增和修改用户信息
    + 可以新增和修改借阅信息
### API说明
| 方法 | 链接 | 说明 | 权限
| :----: |:---:| :---:| :---: |
| GET | /user | 获取全部用户信息 | admin | 
| POST | email=email name=name /user | 新建用户 | admin |
| GET | /user/1 | 获取某条用户信息 | user admin |
| POST | user_name=user_name first_name=first_name pw=pw /user/1 | 修改某条用户信息 | admin |
| GET | /storage | 获取全部图书库存信息 | user admin |
| POST | book=book /storage | 新书入库 | admin |
| GET | /storage/1 | 获取某条库存信息 | user admin |
| POST | book=book inventory=inventory remain=remain /storage/1 | 修改某条库存信息 | admin |
| GET | /history | 获取借阅记录 | user admin |
| POST | /history | 新增借阅记录 | user admin |
| GET | /history/1 | 获取某条借阅记录 | user admin |
| POST | status=status delay=delay /history/1 | 修改某条借阅记录 | user admin |
### 预览说明






