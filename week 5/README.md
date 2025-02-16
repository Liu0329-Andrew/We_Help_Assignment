# 第五周作業:
## Task 2:
● Create a new database named website

![](create.png)

● Create a new table named member, in the website database

![](member.png)
## Task 3:
● INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.

![](insert.png) ![](update_member.png) ![](new_time.png)

● SELECT all rows from the member table

![](select1.png)

● SELECT all rows from the member table, in descending order of time.

![](time_desc.png)

● SELECT total 3 rows, second to fourth, from the member table, in descending order of time

![](update_time.png)

● SELECT rows where username equals to test.

![](test.png)

● SELECT rows where name includes the es keyword

![](keyword.png)

● SELECT rows where both username and password equal to test.

![](keyword2.png)  

● UPDATE data in name column to test2 where username equals to test.

![](update.png)    
## Task 4:
● SELECT how many rows from the member table.

![](count.png)  

● SELECT the sum of follower_count of all the rows from the member table.

![](sum.png)

● SELECT the average of follower_count of all the rows from the member table.

![](avg.png)

● SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.

![](order_limit.png)
## Task 5:
● Create a new table named message, in the website database. designed as below:

![](message.png) ![](reference.png)

● 插入測試資料:

![](insert_message.png)

● SELECT all messages, including sender names. We have to JOIN the member tableto get that.

![](join.png)

● SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.



● Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.



● Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.


