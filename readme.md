# 南阳师范学院滚榜系统

目前可实现功能有：

1、洛谷平台比赛发放气球

2、牛客平台比赛滚榜

3、PTA平台比赛发放气球和滚榜（PTA平台比赛需要费用）

发放气球原理是爬取排行榜信息，结合气球助手送入小票机

滚榜使用的是icpc tools中的resolver，本程序是将比赛提交数据转换为resolver可以使用的数据。因此实现滚榜必须要有完整的比赛提交信息以及封榜功能的OJ

## 使用说明
其中有多个py文件，作用如下：

针对PTA平台：
- resolver_functions.py
    - 主要函数文件，存放要使用到的函数等待调用
- resolver_main.py
    - main文件，比赛结束后，运行此文件即可生成resolver可以使用的数据
    - 生成的数据是ndjson类型的数据（可以有多个对象的json，在vscode中会爆红，但是不影响使用）
    - 生成的数据文件就是resolver.json文件
- resolver_trans.py
    - 在运行main文件前，请先运行此文件生成队伍信息
    - 运行此文件前，请先完成team.xlsx文件，参赛队伍需要完成pta中账号的创建，教师账号需要完成pta比赛中所有队伍进入用户组
    - 生成队伍信息的文件，会根据team.xlsx和pta中的数据，创建为队伍数据文件，保存在./data/team.json文件中
    - team.xlsx已修改，可自动读取到空行结束读取
  
针对牛客平台：

- trans_niuke.py
    - 将牛客昵称和学号写入team.json，用于提交记录判断谁的提交，生成滚榜数据

- resolver_main_niuke.py
    - 将提交信息表格中的信息与team.json对应起来转化成滚榜数据

针对洛谷平台：

- trans_luogu.py
    - 将洛谷昵称写入team.json，用于爬取榜单信息后判断谁过哪个题，位置在哪，发放气球

## 配置文件
在config文件夹中，看介绍修改
- cfg.json
    - problemId: pta的比赛的id，可以直接进入比赛，在连接中找到比赛id
    - cookie: pta中拥有该比赛管理权限的账号的cookie，获取方式为登陆该账号，在f12中找到Application下的cookie并复制下来
    - 其余两个平台只需要填写problemId即可，cookie可不写
- config.json
    - 对于这个文件，会有一些信息没有用到，不用管即可
    - 这里边主要配置一些比赛相关的信息
    - 从上到下依次为
    - 比赛名称（滚榜时显示的比赛名字），比赛开始时间戳，比赛结束时间戳，封榜时长，罚时，题目数量，题目编号，队伍类型（推荐不要改变），组织类型（推荐不要改变），显示状态（推荐不要改变），奖牌数（根据自己情况修改），题目颜色和对应气球颜色（数量必须和题目数对应），图标（应该是ICPC和CCPC两种）,其它选项（推荐不修改）
- contest_judgement.json
    - 主要是评测题目的结果类型，一般不用该就可以使用，因为pta就这些错误信息，内部错误除外
    - 想添加别的错误信息的话可以自己改
    - 字段分别为：id，错误缩写，错误名称，该状态是否算通过，该状态是否罚时
    - 其他两个平台不用修改这个
- contest_language.json
    - 比赛中用到的语言
    - 我们的比赛只让用到了里边的几种
    - 你想添加的话可以加
    - 其它语言统一就用Other Language表示
    - 其他两个平台不用修改这个
- contest_problem.json
    - 题目信息
    - 字段分别为：id，题目标号，题目名称，颜色名称，颜色16进制码
    - 三个平台都需要修改

## 运行环境
### 本系统
JAVA:

- openjdk 22.0.2 2024-07-16

- OpenJDK Runtime Environment (build 22.0.2+9-70)

- OpenJDK 64-Bit Server VM (build 22.0.2+9-70, mixed mode, sharing)

Python: 

- Python 3.12.5

C++: 

- Visual Studio 2022(气球机使用c++语言编写的应用程序，暂时不知道有没有关系，如运行有问题就下载)

java必须配置环境，否则resolver会显示不是可执行的命令

python安装了大量的包，具体忘记了，反正哪里报错就上网搜一下pip install安装一下就行了

### resolver
使用本系统生成数据文件后，还需要使用resolver进行滚榜, resolver 2.5.940版本兼容性较好，其余版本可能会卡住

resolver需要的环境是：

- java8或以上的版本（使用前只需要安装最新版本就可以）

## team.xlsx
该文件为队伍表，每一列都不能少

- 队伍名前加星号表示是打星队伍（中文队伍名字PTA平台可以完全自由发挥，其余两个必须和平台内昵称一模一样）
- 序号一列代码中没有用到，根据自己需求编写就行
- 校内队伍序号一列代码中中没有用到，根据自己需求编写就行
- 赛场和座位号根据自己情况编写：（推荐字母和数字，使用汉字会导致编码出错，显示乱码）
- 表格P列 在什么平台就必须和对应的平台信息一模一样（牛客是牛客学号，PTA和洛谷是昵称。必须完全一样否则生成team.json会出错）

## 程序原理
针对PTA：

主要原理是调用pta的接口，获取到pta中提交列表的数据，然后把pta中得到的提交数据的格式转换为resolver需要的数据格式，队伍信息的获取也是一样的原理

针对洛谷：

爬取榜单，因此需要使用管理员账号作为cookie

针对牛客：

使用牛客提供的提交记录导出工具导出所有比赛提交记录，再将记录转化成滚榜数据

## 程序使用（请按步骤完成）
1. 将配置文件和team.xlsx表格填写完成
2. PTA运行resolver_trans.py，牛客运行trans_niuke.py，洛谷运行trans_luogu.py生成队伍数据(./data/team.json)
3. PTA运行resolver_main.py，牛客运行resolver_main_niuke.py生成resolver要使用的数据（./data/resolver.json）
4. 双击运行resolver2.5文件夹中的awards程序（windows运行bat，linux运行sh）
5. 等待后弹出窗口，在窗口中：disk -> 选中生成的data文件夹下resolver.json文件 -> connect
6. 在新的窗口中，点击Template按钮，通过参数修改奖项配置
7. 在窗口中单击每一个队伍，使用右侧的Edit和Add按钮可以单独修改和添加某一个队伍的奖项
    - 最好是在Template设置金银铜，最快解题奖
    - 类似于最佳女队，专科金银铜（数量比较少）等特殊奖项，可以手动添加
    - 如果专科队伍较多，可以尝试修改代码中的生成group的部分，将专科和本科换分为不同的group，然后根据group分别办法金银铜（我没有实现，需要你自己改）
8. 点击右侧Save event_feed会生成最终滚榜使用的json文件（不出意外应该叫做event-feed.ndjson）
9. 将event-feed.ndjson拖到resolver.bat即可运行，直接双击无法运行（windows运行bat，linux运行sh）
10. 稍微等待后，就可以开始滚榜

## 滚榜程序的使用

滚榜程序运行时可以指定文件夹运行，可以在其中添加队伍图片，各种logo等，想要的话需要自己百度研究一下，本系统没有这些，直接使用的event-feed.json文件运行的

滚榜工具使用按键我也是查的，但是感觉不太对，放在这里仅供参考，可以自己阅读官方文件（当时时间紧任务重，我没时间看）

- ctrl+q 停止
- 空格/f 下一步
- r 上一步
- +/= 加速
- -/_ 减速

334344865这是domejudge的qq群，里边的同学们都很热情，关于resolver有问题可以去里边询问

## 气球小票机
从Github上获取并修改，可连接一台小票打印机，比赛时自动获取提交列表打印小票给志愿者发气球，使用方法在PTA_Balloon_Print-main下README.md内