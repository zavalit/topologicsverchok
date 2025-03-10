import bpy
from bpy.props import IntProperty, FloatProperty, StringProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

from topologic import Dictionary, Attribute, AttributeManager, IntAttribute, DoubleAttribute, StringAttribute
import cppyy


def processItem(item):
	values = item.Values()
	returnList = []
	for aValue in values:
		s = cppyy.bind_object(aValue.Value(), 'StringStruct')
		returnList.append(str(s.getString))
	return returnList

def recur(input):
	output = []
	if input == None:
		return []
	if isinstance(input, list):
		for anItem in input:
			output.append(recur(anItem))
	else:
		output = processItem(input)
	return output
	
class SvDictionaryValues(bpy.types.Node, SverchCustomTreeNode):
	"""
	Triggers: Topologic
	Tooltip: Outputs the list of values of the input Dictionary   
	"""
	bl_idname = 'SvDictionaryValues'
	bl_label = 'Dictionary.Values'
	def sv_init(self, context):
		self.inputs.new('SvStringsSocket', 'Dictionary')
		self.outputs.new('SvStringsSocket', 'Values')

	def process(self):
		if not any(socket.is_linked for socket in self.outputs):
			return
		if not any(socket.is_linked for socket in self.inputs):
			return
		
		inputs = self.inputs['Dictionary'].sv_get(deepcopy=False)
		outputs = []
		for anInput in inputs:
			outputs.append(recur(anInput))
		if len(outputs) == 1:
			outputs = outputs[0]
		self.outputs['Values'].sv_set(outputs)

def register():
	bpy.utils.register_class(SvDictionaryValues)

def unregister():
	bpy.utils.unregister_class(SvDictionaryValues)
