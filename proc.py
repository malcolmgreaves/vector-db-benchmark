import sys
import json

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        with open(line,'rt') as rt:
            j = json.load(rt)

        del j['results']['latencies']
        del j['results']['precisions']
        x = j['results']
        
        with open(f"{line}-slim",'wt') as wt:
            json.dump(x, wt, indent=2)



