#!/bin/bash
for i in {1..50}
do
    touch "/home/guillermo/test/file_${i}.txt"
    sudo chown user1:group1 "/home/guillermo/test/file_${i}.txt"
    touch "/opt/data/test/file_${i}.txt"
    sudo chown user6:group3 "/opt/data/test/file_${i}.txt"
done

for i in {50..100}
do
    touch "/home/guillermo/test/file_${i}.txt"
    sudo chown user2:group2 "/home/guillermo/test/file_${i}.txt"
    touch "/opt/data/test/file_${i}.txt"
    sudo chown user7:group4 "/opt/data/test/file_${i}.txt"
done

for i in {100..150}
do
    touch "/home/guillermo/test/file_${i}.txt"
    sudo chown user3:group2 "/home/guillermo/test/file_${i}.txt"
    touch "/opt/data/test/file_${i}.txt"
    sudo chown user8:group5 "/opt/data/test/file_${i}.txt"
done

for i in {150..200}
do
    touch "/home/guillermo/test/file_${i}.txt"
    sudo chown user4:group3 "/home/guillermo/test/file_${i}.txt"
    touch "/opt/data/test/file_${i}.txt"
    sudo chown user9:group5 "/opt/data/test/file_${i}.txt"
done

for i in {200..300}
do
    touch "/home/guillermo/test/file_${i}.txt"
    sudo chown user5:group4 "/home/guillermo/test/file_${i}.txt"
    touch "/opt/data/test/file_${i}.txt"
    sudo chown user10:group1 "/opt/data/test/file_${i}.txt"
done