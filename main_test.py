from FlowNet import FlowNet

max_flow_expected = [23, 8, 7, 16, 28]
file_paths = ["fig42.csv","test1.csv","test2.csv","test3.csv","test4.csv"]
i = 0
for file_path in file_paths:
    n = FlowNet("TestCase/"+file_path)
    source = list(n.G.nodes)[0]
    sink = list(n.G.nodes)[len(n.G.nodes)-1]
    n.compute_max_flow()

    print("------------------")
    if n.get_flow() == max_flow_expected[i]:
        print("TestCase: "+file_path+" [OK]")
    else:
        print("TestCase: "+file_path+" [FAILED]")

    print("Max Flow: ", n.get_flow())
    i += 1
