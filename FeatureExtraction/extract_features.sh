ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9
cd storm
pwd
parallel  -j 7 -a xaa python flow.py
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

parallel  -j 7 -a xaa python convo.py
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

parallel  -j 7 -a xab python flow.py
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

parallel  -j 7 -a xab python convo.py
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

parallel  -j 7 -a xac python flow.py
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

parallel  -j 7 -a xac python convo.py
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

parallel  -j 7 -a xad python flow.py
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

parallel  -j 7 -a xad python convo.py
cd ..
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9
cd waledac
pwd
parallel  -j 7 -a *.txt python flow.py
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

parallel  -j 7 -a *.txt python convo.py
cd ..
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9

pwd
echo 'done'

