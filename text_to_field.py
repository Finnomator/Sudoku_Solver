import json
import os 


this_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
abc = "abcdefghi"

field = {}

for l in abc:
    print("Enter row "+l+":")
    while True:
        toinput = list(input())
        if len(toinput) != 9:
            print("false length")
        else:
            try:
                toinput = list(map(int,toinput))
                break
            except:
                print("not numbers")
    
    field.update({l: toinput})

json.dump(field,open(this_path+"field.json","w"),indent=4)