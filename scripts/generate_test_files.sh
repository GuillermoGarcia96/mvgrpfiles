#!/bin/bash
for i in {1..500}
do
    touch "/home/guillermo/test/file_${i}.txt"
    chown user1:group1 "/home/guillermo/test/file_${i}.txt"
    sudo touch "/opt/data/test/file_${i}.txt"
    sudo chown user6:group3 "/opt/data/test/file_${i}.txt"
done

for i in {500..1000}
do
    touch "/home/guillermo/test/file_${i}.txt"
    chown user2:group2 "/home/guillermo/test/file_${i}.txt"
    sudo touch "/opt/data/test/file_${i}.txt"
    sudo chown user7:group4 "/opt/data/test/file_${i}.txt"
done

for i in {1000..1500}
do
    touch "/home/guillermo/test/file_${i}.txt"
    chown user3:group2 "/home/guillermo/test/file_${i}.txt"
    sudo touch "/opt/data/test/file_${i}.txt"
    sudo chown user8:group5 "/opt/data/test/file_${i}.txt"
done

for i in {1500..2000}
do
    touch "/home/guillermo/test/file_${i}.txt"
    chown user4:group3 "/home/guillermo/test/file_${i}.txt"
    sudo touch "/opt/data/test/file_${i}.txt"
    sudo chown user9:group5 "/opt/data/test/file_${i}.txt"
done

for i in {2000..3000}
do
    touch "/home/guillermo/test/file_${i}.txt"
    chown user5:group4 "/home/guillermo/test/file_${i}.txt"
    sudo touch "/opt/data/test/file_${i}.txt"
    sudo chown user10:group1 "/opt/data/test/file_${i}.txt"
done