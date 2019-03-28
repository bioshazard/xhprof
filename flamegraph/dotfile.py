
# N59[shape=box , label="file_exists\nInc: 0.220 ms (1.5%)\nExcl: 0.220 ms (1.5%)\n21 total calls", width=0.6, height=0.4, fontsize=20];
# N60[shape=box , label="PDO::__construct\nInc: 0.405 ms (2.8%)\nExcl: 0.405 ms (2.8%)\n1 total calls", width=1.2, height=0.8, fontsize=26];
# N4 -> N0[arrowsize=1, color=grey, style="setlinewidth(1)", label="15 calls", headlabel="1.6%", taillabel="100.0%" ];
# N32 -> N1[arro

import re, mmap, sys

with open("/tmp/dotfile.txt", 'r+') as fp:
    data = mmap.mmap(fp.fileno(), 0)
    boxes = re.findall(r'(N[0-9]+)\[.*?label="([0-9A-Za-z_:{}]+).*?(\d+\.\d+) ms.*?(\d+) total calls?', data)
    arrows = re.findall(r'(N[0-9]+) -> (N[0-9]+)\[.*?label="(\d+) calls?"', data)
    #print(boxes)
    # print(arrows)

call_map = {}
for box in boxes:
    call_map[box[0]] = {
        "label": box[1],
        "ns": int(float(box[2])*1000), # convert to ns
        "calls": int(box[3])
    }

parent_child_map = {}
for arrow in arrows:
    if arrow[0] not in parent_child_map:
        parent_child_map[arrow[0]] = { }

    parent_child_map[arrow[0]][arrow[1]] = int(arrow[2])


class FlamePrep:
    def __init__(self, fullMap, nodeMeta):
        self.fullMap = fullMap # really just for global access in the recursive function
        self.nodeMeta = nodeMeta # really just for global access in the recursive function

    def resolveName(self, node):
        return self.nodeMeta[node]["label"]

    def doTraversal(self):
        #XHProfRun = self.fullMap["N34"] # Magic number for now for XHProf run. Will detect later.
        self.recursiveTraversal("N34")

    # Depth first traversal to last child
    def recursiveTraversal(self, parentNode, path=[]):

        # Loop through child nodes

        for childNode, callCnt in self.fullMap[parentNode].items():
            newPath = path + [childNode]

            #print("Loop on %s" % self.resolveName(childNode), "at", path)

            # If this node has children of its own...
            if childNode in self.fullMap.keys():
                self.recursiveTraversal(childNode, newPath)
            else:
                # We have reached depth, print path and endpoint
                #print(path)
                flameResult = []
                for pathNode in newPath:
                    flameResult.append(self.resolveName(pathNode))
                # flameResult.append("%s %d" % (self.nodeMeta[childNode]["label"], self.nodeMeta[childNode]["calls"]))
                #flameResult.append(self.nodeMeta[childNode]["label"])

                # Call count
                print("%s %f" % (";".join(flameResult), self.nodeMeta[childNode]["calls"]) )

                # Call count Icecicle
                # flameResult.reverse()
                # print("%s %f" % (";".join(flameResult), self.nodeMeta[childNode]["calls"]) )

                # NS
                #print("%s %f" % (";".join(flameResult), self.nodeMeta[childNode]["ns"]) )

                # NS Icecicle
                # flameResult.reverse()
                # print("%s %f" % (";".join(flameResult), self.nodeMeta[childNode]["ns"]) )


        # TODO: Print with final call count if any left




myFlame = FlamePrep(parent_child_map, call_map)
myFlame.doTraversal()
