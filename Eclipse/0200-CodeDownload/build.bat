"c:\Program Files\Java\jdk1.6.0_20\bin\jar.exe" cmf Launch4j\CodeDownload.mf main\main.jar CodeDownload*.class HexFilter*.class
"c:\Program Files\Java\jdk1.6.0_20\bin\jar.exe" cmf Launch4j\CodeDownload.mf CodeDownload.jar main\main.jar lib\RXTXcomm.jar lib\rxtxSerial.dll
mkdir boot
cd boot
"c:\Program Files\Java\jdk1.6.0_20\bin\jar.exe" -xvf ..\one-jar-boot-0.95.jar
"c:\Program Files\Java\jdk1.6.0_20\bin\jar.exe" -uvfm ..\CodeDownload.jar boot-manifest.mf com doc
move ..\CodeDownload.jar ..\Launch4j
cd ..
