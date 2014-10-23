import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

class ScenarioAction:
    def __init__(self):
            pass
    def Print(self):
            print self.ToString()
    def ToString(self):
            return "BaseAction"
    def LoadElement(self, element):
            return True
    def SaveElement(self, parent_element):
            pass
    def PutDataIntoListbox(self, array):
            array.append(self.ToString())
class ActionDefineActor(ScenarioAction):
    def LoadElement(self, element):
        if ("actor_id" in element.attrib) & ("actor_name" in element.attrib):
                self.actor_id = element.attrib["actor_id"]
                self.actor_name = element.attrib["actor_name"]
                return True
        else:
                return False
    def ToString(self):
            return "[def_actor] actor_id: {0}, actor_name: {1}".format(self.actor_id, self.actor_name)
    def SaveElement(self, parent_element):
            element = Element("def_actor", {"actor_id":self.actor_id, "actor_name":self.actor_name})
            parent_element.append(element)
    def CreateNew(self, actor_id, actor_name):
            self.actor_id = actor_id
            self.actor_name = actor_name
class ActionDialog(ScenarioAction):
    def LoadElement(self, element):
        if "actor_id" in element.attrib:
                self.actor_id = element.attrib["actor_id"]
                self.text = element.text
                return True
        else:
                return False
    def ToString(self):
            return "[dialog] actor_id: {0}, text: {1}".format(self.actor_id, self.text)
    def SaveElement(self, parent_element):
            element = Element("dialog", {"actor_id":self.actor_id})
            element.text = self.text
            parent_element.append(element)
    def CreateNew(self, actor_id, text):
            self.actor_id = actor_id
            self.text = text
class ActionSet(ScenarioAction):
    def __init__(self):
            ScenarioAction.__init__()
            self.child_action_list = []
    def LoadElement(self, root):
            for element in root:
                    print "Set   LoadElement:=====>", element.tag
                    if element.tag in self.type_map:
                            tempObject = self.type_map[element.tag]()
                            loadResult = tempObject.LoadElement(element)
                            if loadResult == True:
                                    self.action_list.append(tempObject)
                            else:
                                    print "Load element failed: ", element.tag
                    else:
                            print "Can't decode element: ", element.tag
    def ToString(self):
            return ""
    def SaveElement(self, actor_id, text):
            pass
    def CreateNew(self):
            pass
class ScenarioObject:
    type_map = {
        "def_actor":ActionDefineActor,
        "dialog":ActionDialog
    }
    def __init__(self):
            self.action_list = []
            self.uid = ""
    def Load(self, path):
            print "load file path:",path
            tree = ET.parse(path)
            root = tree.getroot()
            
            # check root element
            if root.tag != "scenario":
                    return False
            
            # load root attrs
            self.uid = root.attrib["uid"]
            
            # load elements
            for element in root:
                    print "LoadElement:=====>", element.tag
                    if element.tag in self.type_map:
                            tempObject = self.type_map[element.tag]()
                            loadResult = tempObject.LoadElement(element)
                            if loadResult == True:
                                    self.action_list.append(tempObject)
                            else:
                                    print "Load element failed: ", element.tag
                    else:
                            print "Can't decode element: ", element.tag
            
            self.Print()
            return True
    def Save(self, path):
            print "save file path:", path
            root = Element("scenario")
            tree = ElementTree(root)
            root.attrib["uid"] = self.uid
            for action in self.action_list:
                    action.SaveElement(root)
            self.indent(root)
            tree.write(path, 'utf-8')
    # used to format xml file
    def indent(self, elem, level=0):
            i = "\n" + level*"\t"
            if len(elem):
                    if not elem.text or not elem.text.strip():
                            elem.text = i + "\t"
                    if not elem.tail or not elem.tail.strip():
                            elem.tail = i
                    for elem in elem:
                            self.indent(elem, level+1)
                    if not elem.tail or not elem.tail.strip():
                            elem.tail = i
            else:
                    if level and (not elem.tail or not elem.tail.strip()):
                            elem.tail = i
    def Reset(self):
            del self.action_list[:]
            self.uid = ""
    def Print(self):
            print "ScenarioObjectData:"
            print "uid = ", self.uid
            for action in self.action_list:
                    action.Print()
    def GetListboxArray(self):
            array = []
            for action in self.action_list:
                    action.PutDataIntoListbox(array)
            return array