set str=%cd%
set str=%str:~-4%
if /i %str%==\bin cd ..
HexMerge.exe -boot bin\HCS08MiniBoot.asm.slow.8k.sx -app bin\1001.sx -out bin\1001Boot.sx -smsrec bin\1001Upgrade.sx
