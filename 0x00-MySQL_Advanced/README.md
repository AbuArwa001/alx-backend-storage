# 0x00. MySQL Advanced

## Concepts
This project covers advanced SQL concepts. The main focus areas include:

- Advanced SQL

## Resources
To complete this project, refer to the following resources:

- [MySQL cheatsheet](https://devhints.io/mysql)
- [MySQL Performance: How To Leverage MySQL Database Indexing](https://www.percona.com/blog/2020/05/27/mysql-performance-how-to-leverage-mysql-database-indexing/)
- [Stored Procedure](https://dev.mysql.com/doc/refman/5.7/en/stored-programs-defining.html)
- [Triggers](https://dev.mysql.com/doc/refman/5.7/en/triggers.html)
- [Views](https://dev.mysql.com/doc/refman/5.7/en/create-view.html)
- [Functions and Operators](https://dev.mysql.com/doc/refman/5.7/en/functions.html)
- [Trigger Syntax and Examples](https://dev.mysql.com/doc/refman/5.7/en/trigger-syntax.html)
- [CREATE TABLE Statement](https://dev.mysql.com/doc/refman/5.7/en/create-table.html)
- [CREATE PROCEDURE and CREATE FUNCTION Statements](https://dev.mysql.com/doc/refman/5.7/en/create-procedure.html)
- [CREATE INDEX Statement](https://dev.mysql.com/doc/refman/5.7/en/create-index.html)
- [CREATE VIEW Statement](https://dev.mysql.com/doc/refman/5.7/en/create-view.html)

## Learning Objectives
By the end of this project, you should be able to explain the following concepts without assistance:

- How to create tables with constraints
- How to optimize queries by adding indexes
- How to implement stored procedures and functions in MySQL
- How to implement views in MySQL
- How to implement triggers in MySQL

## Requirements
- All files will be executed on Ubuntu 18.04 LTS using MySQL 5.7 (version 5.7.30).
- Files should end with a new line.
- SQL queries should have a comment just before them.
- Files should start with a comment describing the task.
- All SQL keywords should be in uppercase (e.g., SELECT, WHERE).
- A `README.md` file is mandatory.
- File lengths will be tested using `wc`.

## More Info

### Comments for SQL Files
Example of how to structure your SQL files with comments:

```sql
-- 3 first students in the Batch ID=3
-- because Batch 3 is the best!
SELECT id, name FROM students WHERE batch_id = 3 ORDER BY created_at DESC LIMIT 3;
