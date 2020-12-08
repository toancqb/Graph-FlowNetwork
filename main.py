from FlowNet import FlowNet
import sys

if len(sys.argv) != 5:
    print(str(sys.argv))
    sys.exit("Invalid Arguments\nUsage: python3 main.py fileName.csv node1 node2 capacity")

n = FlowNet(sys.argv[1])

n.compute_max_flow()

print(n.get_flow())

n.export("graph_before.png")

n.update(sys.argv[2], sys.argv[3], int(sys.argv[4]))

print(n.get_flow())

n.export("graph_after.png")
