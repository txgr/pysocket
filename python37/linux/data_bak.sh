#!/bin/bash
export LANG=en_US.UTF-8
BakDir=/home/mysql/backup
LogFile=/home/mysql/backup/bak.log
Date=`date +%Y%m%d`
Begin=`date +"%Y年%m月%d日 %H:%M:%S"`
cd $BakDir
DumpFile=$Date.sql
GZDumpFile=$Date.sql.tgz
mysqldump -uroot -p root aass@1122 --all-databases --flush-logs --delete-master-logs --single-transaction > $DumpFile
tar -czvf $GZDumpFile $DumpFile
rm $DumpFile

count=$(ls -l *.tgz |wc -l)
if [ $count -ge 5 ]
then
file=$(ls -l *.tgz |awk '{print $9}'|awk 'NR==1')
rm -f $file
fi
#只保留过去四周的数据库内容

Last=`date +"%Y年%m月%d日 %H:%M:%S"`
echo 开始:$Begin 结束:$Last $GZDumpFile succ >> $LogFile
cd $BakDir/daily
rm -f *