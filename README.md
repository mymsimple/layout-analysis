# layout-analysis
card business demo

# 2020.06.15创建
本项目用深度学习mask-rcnn和模板匹配等方法，实现各种卡证类和文档类的商务demo。
以身份证为例，方法如下：
 - 第一步：先用mask-rcnn预测出类别和区域，返回box和mask
 - 第二步：用mask值确定身份证边框的四点坐标
 - 第三步：通过四点坐标做仿射矫正抠图
 - 第四步：套模板，直接返回结果
 
 

