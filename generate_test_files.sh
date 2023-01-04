#!/bin/bash
for i in {1..50}
do
    echo "some text" > "test_files/file_${i}.txt"
    sudo chown univention:univention "test_files/file_${i}.txt"
done

for i in {50..100}
do
    echo "some text" > "test_files/file_${i}.txt"
    sudo chown testuser:univention "test_files/file_${i}.txt"
done