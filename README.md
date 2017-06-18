# django_blog


### 通过Python3.6、django1.11、sqlit3、bootstrap、建立个人blog
### 预览图：

![](https://ooo.0o0.ooo/2017/06/18/59463c7b3860e.png)

### 如何使用：

1. 在vps上安装前置环境：pip install -r requirement.txt
2. clone master下的分之 git clone https://github.com/Ehco1996/django_blog.git
3. 生成数据库文件: 首先：python manage.py makemigration 其次：python manage.py migrate
4. 生成管理员账号：python manage.py createsuperuser
5. 生成搜索缓存：python manage.py rebulid_index
6. 配置uwgsi.ini文件
7. 配置niginx文件
8. 让项目跑起来：uwsgi uwsgi


### 自定义blog内容：

* bolg的模板放在根目录的 templates/
* 修改templates/base.html 就能粗略的自定义bolg的样式
* 背景音乐在static/blog/media/ 下
* 其他细节请自行定制和修改
  


### 开发日志：
 day01 创建blog项目，并设置好中文与时区
 day02 编写blog 应用的的主要url逻辑，django的admin后台套用与扩展
 day03 编写首页模板 已经数据库的model 主要有三个类 post（文章主体） category 以及 tag
 day04 套用网页模板blackandwhite 编写分类 归档 最近更新 界面
 day05 心情不好，显示器太小了，太贵买不起 卒
 day06 恢复更新  增加最基本的评论功能，并修复侧边栏bug
 day07 增加blog的bmg ，并实现用js按钮和bootstrap 布局开关
 day08 尝试使用畅言，失败。。。需要先部署备案才能使用，正在研究 uwsgi +nginx 上线中，vps解决Python版本问题，
 day09  购买域名 www.ehcoblog.ml 并使用cloudxns云解析。初步将本地网站迁移至vps
 day10  1. 弃用畅言，不得不说多说倒闭了是有理由的，这个东西不好商业化，没钱赚，服务器就垃圾，垃圾就不想用，不想用就没广告，没广告就更垃圾啊！ 改用友言。 2. 排除一些git文件
 day11  1. 增加首页页码 ，文章摘要，增加detail页面的headimg 和上下文关联
 day12  修复归档和分类页面的bug
 day13  定制个性化拓展计划，更新readme。
 day14  增加粗略的搜索页面。
 day15  增加文章目录的侧边栏
 day16  使用autocjs 生成动态侧边栏。修改首页logo,增加文章内容的排版css，对中文有更好的支持
 day17  居然忘记更新readme了。最近增加了漂亮的页码显示，comment模块雏形，自动生成文章摘要，修复上下文显示bug
 day18  用haystack实现全文搜索与关键字高亮 ，重新排版template文件夹，使得继承更加方便，更新readme
 day19  bolg基本开发完成，整理开发日志，写出使用说明。