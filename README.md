#TSP(MTZ约束）代码优化 
这个优化版的代码做了如下改进：
将distance_calculation函数简化为haversine_distance，使用pandas DataFrame更直接地访问经纬度。
在创建距离矩阵时避免了重复计算对称项。
使用列表推导式生成index_tplst，更加简洁。
对流入和流出约束表达式进行了简化。
输出结果显示部分格式化，使得输出信息更为清晰。
