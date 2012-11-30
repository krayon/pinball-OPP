set str=%cd%
set str=%str:~-4%
if /i %str%==\bin cd ..
HexMerge.exe -boot bin\HCS08MiniBoot.asm.32k.sx -app bin\1008.sx -out bin\1008Boot.sx -smsrec bin\1008Upgrade.sx
