Note: Please notice that this file is for personal reference only. Some sentences are directly copied from the internet without any reference simply for readability. If you feel I have violated your copyright, please contact me and I will either remove what I have pasted here, or add references. Thank you! 

---

# 8/27/2019 

## What do backend Developers do? 
The key job role of a backend developer is to ensure that the data or services requested by a user through the frontend system or software are delivered through programmatic means. 

Backend developers also create and maintain the core databases, data and application program interfaces (APIs) to other backend processes.

In addition to writing new features, backend developers often have to conduct maintenance while testing and debugging systems.

## 自己的一个提问

**问：** 

我需要做一个Web App，目前欲想的功能就是，输入一个excel文件，它能通过我已经训练好的Random Forest模型、根据每一行的 given variables 自动分类这一行的data point属于哪个category，然后生成一个新的excel文件记录分类结果

我的问题是，这用ReactJS能全实现吗？（之前有一小段前端开发的实战经验，但挺皮毛的。而后端几乎没什么经历）需要用到Backend的东西吗？如果需要，用Django可以吗？

另，有直接能把Python的model转换成 Javascript的方法吗？或者有啥办法能直接在网页上embed我用Python训练出来的模型吗？


**答：**
1. 理论上是可以纯前端实现的，但是有两个问题，首先ReactJS处理大一点的文件或者逻辑时，可能会卡到爆。其次，即使不太卡，前端也不太适合做这些（我猜和programming style、convention有关）

2. 引用柯锦，通常前端接收数据parse to json然后传给后端，后端处理得到结果传到前端再export to Excel

3. Flask。可以直接用Python、pandas做表格然后用Flask来拼接前后端。把模型什么的全部放在后端，结果用Python Flask传到前端，能直接用HTML显示出来，都不用JS。但Flask的缺点就是可能有点丑，前端的layout很死板，所以可以加一些CSS或者用React搞得漂亮点

4. JS现在也比较万能，如果后台用node写，一些情况下性能甚至比Python好。JS是可以做机器学习的，比如: tensorflow.org/js 