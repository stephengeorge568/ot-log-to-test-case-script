import sys
import re
# C:\Users\steph\Desktop
class Change:
    def __init__(self, text, identity, sc, ec, sl, el, revId, name):
        self.text = text
        self.identity = identity
        self.sc = sc
        self.ec = ec
        self.sl = sl
        self.el = el
        self.revId = revId
        self.name = name

    def createHistory(self):
        return f"\t\tStringChangeRequest {self.name} = new StringChangeRequest(\"{self.text}\", new MonacoRange({self.sc},{self.ec},{self.sl},{self.el}), {self.revId}, {self.identity});"


inputFile = sys.argv[1]

textStart = re.escape("text=\'")
textEnd = re.escape("\', identity=")

identityStart = re.escape("identity=\'")
identityEnd = re.escape("\', rangeSC=")

scStart = re.escape("rangeSC=")
scEnd = re.escape(", rangeEC")

ecStart = re.escape("rangeEC=")
ecEnd = re.escape(", rangeSL")

slStart = re.escape("rangeSL=")
slEnd = re.escape(", rangeEL")

elStart = re.escape("rangeEL=")
elEnd = re.escape(", revID")

revIdStart = re.escape("revID=")
revIdEnd = re.escape(", setID")

changes = []

with open(inputFile, 'r') as file:
    index = 1
    while True:
        line = file.readline()
        
        if not line:
            break
        if line == '||||':
            break
        if "SCR T" in line:
            change = Change(
                re.search('%s(.*)%s' % (textStart, textEnd), line).group(1),
                re.search('%s(.*)%s' % (identityStart, identityEnd), line).group(1),
                re.search('%s(.*)%s' % (scStart, scEnd), line).group(1),
                re.search('%s(.*)%s' % (ecStart, ecEnd), line).group(1),
                re.search('%s(.*)%s' % (slStart, slEnd), line).group(1),
                re.search('%s(.*)%s' % (elStart, elEnd), line).group(1),
                re.search('%s(.*)%s' % (revIdStart, revIdEnd), line).group(1),
                f"history{index}")
            changes.append(change)
            index += 1

print("\t@Test\n\tvoid transform_ENTERNAME() {")
print("\t\t// Edit this request with what change you want to test...")
print("\t\tStringChangeRequest request = new StringChangeRequest("", new MonacoRange(), ))")
print("\n\t\t// NOTE: these are the historical requests post transformation...")
chang: Change
historyNameSequence = ""
for change in changes:
    print(change.createHistory())
    historyNameSequence += change.name + ','
    

print("\n\t\tArrayList<StringChangeRequest> historyList = new ArrayList<>();")



historyAddAll = f"\t\thistoryList.addAll(Arrays.asList(new StringChangeRequest[]{{ {historyNameSequence} }}));"
print(historyAddAll)

print("\n\t\tHashMap<Integer, ArrayList<StringChangeRequest>> history = new HashMap<>();")
print("\t\thistory.put(1, historyList);")

print("\n\t\tStringChangeRequest expectedResult = new StringChangeRequest("", new MonacoRange(), ))")
print("\t\tArrayList<StringChangeRequest> transformedRequests = OperationalTransformation.transform(request, history);")

print("\n\t\tSystem.out.println(\"Transformed: \" + transformedRequests.get(0).toString());")
print("\t\tSystem.out.println(\"Expected:    \" + expectedResult.toString());")

print("\n\t\tassertEquals(true, transformedRequests.get(0).isEqual(expectedResult));")
print("\t\tassertEquals(true, transformedRequests.get(1) == null);")
print("\t}")