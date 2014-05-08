cd storm
pwd
parallel  -j 15 -a *.txt python sort_csv.py
cd ..
cd waledac
pwd
parallel  -j 15 -a *.txt python sort_csv.py 
cd ..
cd zeus
pwd
parallel   -j 15 -a *.txt python sort_csv.py 
cd ..
cd clean
pwd
parallel  -j 15 -a *.txt python sort_csv.py 
cd ..
pwd
echo 'done'
