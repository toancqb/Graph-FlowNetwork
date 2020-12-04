from FlowNet import FlowNet

n = FlowNet("TestCase/fig42.csv")


# print(len(n.G.nodes))
# print(n.G.nodes)
# print(n.G.edges)
source = list(n.G.nodes)[0]
sink = list(n.G.nodes)[len(n.G.nodes)-1]
# print(source, sink)
n.compute_max_flow()

print("Max Flow: ", n.get_flow())

n.update('a', 'c', 9)

print("Max Flow: ", n.get_flow())

n.show()
