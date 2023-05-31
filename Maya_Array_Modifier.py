import maya.cmds as cmds
class ArrayCls:
	#Constructor
	def __init__(self):
		self.window="ArrayWindow"
		self.title="Array Modifier"

		if cmds.window(self.window,q=1,ex=1):
			cmds.deleteUI(self.window)

		#Create New Window
		self.window=cmds.window(self.window,t=self.title)
		cmds.columnLayout(adj=1)
		cmds.text(hlc=(1,0,0),l="Array Modifier Created By Hossam Eldin Nasser")
		cmds.separator(h=20)
		self.mesh_btn=cmds.textFieldButtonGrp(bl="Set",l="Mesh",bc=self.setMesh)
		self.ary_num=cmds.intSliderGrp(l='Number',f=1,fmx=99999999,cc=self.UpdateArray,dc=self.UpdateArray)
		self.ofst_const=cmds.floatFieldGrp(l="Constant Offset",nf=3,s=0.01,cc=self.UpdateArray,dc=self.UpdateArray)
		self.ofst_rltv=cmds.floatFieldGrp(l="Relative Offset",nf=3,v1=1,s=0.01,cc=self.UpdateArray,dc=self.UpdateArray)
		self.ofst_msh=cmds.textFieldButtonGrp(bl="Set",l="Mesh Offset",bc=self.setOffsetMesh)
		self.crv=cmds.textFieldButtonGrp(bl="Set",l="Curve",bc=self.setCurve)
		self.Curve=""
		#Show Window
		cmds.showWindow()

	def setMesh(self):
		self.ArrayMesh=cmds.ls(sl=1)[0]
		self.ArrayMeshName=self.ArrayMesh
		self.mesh_btn=cmds.textFieldButtonGrp(self.mesh_btn,e=1,tx=self.ArrayMesh)

	def setOffsetMesh(self):
		self.OffsetMesh=cmds.ls(sl=1)[0]
		self.ofst_msh=cmds.textFieldButtonGrp(self.ofst_msh,e=1,tx=self.OffsetMesh)

	def setCurve(self):
		self.Curve=cmds.ls(sl=1)[0]
		if cmds.nodeType(self.Curve)=="nurbsCurve":
			self.crv=cmds.textFieldButtonGrp(self.crv,e=1,tx=self.Curve)
		elif cmds.nodeType(self.Curve)=="transform":
			if cmds.nodeType(cmds.listRelatives(self.Curve)[0])=="nurbsCurve":
				self.crv=cmds.textFieldButtonGrp(self.crv,e=1,tx=self.Curve)
			else:
				self.crv=cmds.textFieldButtonGrp(self.crv,e=1,tx="Select a C U R V E")

	def UpdateArray(self,*args):
		if cmds.objExists(cmds.textFieldButtonGrp(self.mesh_btn,q=1,tx=1)):					#Array Mesh Text
			if cmds.objExists(self.ArrayMeshName+"_Array"):
				cmds.delete(self.ArrayMeshName+"_Array")

			self.ArrayGRP=cmds.group(n=self.ArrayMeshName+"_Array",em=1)
			#Getting Array Attributes
			##Constant Coordinates##
			self.ConstantX=cmds.floatFieldGrp(self.ofst_const,q=1,v1=1)
			self.ConstantY=cmds.floatFieldGrp(self.ofst_const,q=1,v2=1)
			self.ConstantZ=cmds.floatFieldGrp(self.ofst_const,q=1,v3=1)
			self.InstancesNum=cmds.intSliderGrp(self.ary_num,q=1,v=1)
			##Relative Coordinates##
			self.SizeX=cmds.exactWorldBoundingBox(self.ArrayMesh)[3]\
							-cmds.exactWorldBoundingBox(self.ArrayMesh)[0]		#Max X-Min X
			self.SizeY=cmds.exactWorldBoundingBox(self.ArrayMesh)[4]\
							-cmds.exactWorldBoundingBox(self.ArrayMesh)[1]		#Max Y-Min Y
			self.SizeZ=cmds.exactWorldBoundingBox(self.ArrayMesh)[5]\
							-cmds.exactWorldBoundingBox(self.ArrayMesh)[2]		#Max Z-Min Z
			self.RelativeX=cmds.floatFieldGrp(self.ofst_rltv,q=1,v1=1)
			self.RelativeY=cmds.floatFieldGrp(self.ofst_rltv,q=1,v2=1)
			self.RelativeZ=cmds.floatFieldGrp(self.ofst_rltv,q=1,v3=1)
			##Offset Mesh Coordination##
			if cmds.objExists(cmds.textFieldButtonGrp(self.ofst_msh,q=1,tx=1)):
				self.ofst_msh_tX=cmds.xform(self.OffsetMesh,q=1,t=1)[0]
				self.ofst_msh_tY=cmds.xform(self.OffsetMesh,q=1,t=1)[1]
				self.ofst_msh_tZ=cmds.xform(self.OffsetMesh,q=1,t=1)[2]
				self.ofst_msh_rX=cmds.xform(self.OffsetMesh,q=1,ro=1)[0]
				self.ofst_msh_rY=cmds.xform(self.OffsetMesh,q=1,ro=1)[1]
				self.ofst_msh_rZ=cmds.xform(self.OffsetMesh,q=1,ro=1)[2]
				self.ofst_msh_sX=cmds.xform(self.OffsetMesh,q=1,s=1)[0]
				self.ofst_msh_sY=cmds.xform(self.OffsetMesh,q=1,s=1)[1]
				self.ofst_msh_sZ=cmds.xform(self.OffsetMesh,q=1,s=1)[2]
			else:
				self.ofst_msh_tX=0
				self.ofst_msh_tY=0
				self.ofst_msh_tZ=0
				self.ofst_msh_rX=0
				self.ofst_msh_rY=0
				self.ofst_msh_rZ=0
				self.ofst_msh_sX=1
				self.ofst_msh_sY=1
				self.ofst_msh_sZ=1
	
			#Duplication Instance
			##For loop on ArrayNumber Attr##
			for i in range(0,self.InstancesNum):
				if i==0:
					self.DuplicatedObj=cmds.duplicate(self.ArrayMesh,ilf=1)
					cmds.parent(self.DuplicatedObj,self.ArrayGRP)
				else:
					self.DuplicatedObj=cmds.duplicate(self.CurrentMesh,ilf=1)
				
				self.CurrentMesh=self.DuplicatedObj
				if cmds.objExists(self.Curve):
					MotionPathNode=cmds.pathAnimation(self.CurrentMesh, c=self.Curve ,f=1,fa="x",fm=1,ua="y",stu=0,su=1,eu=1)
					print(str(i)+"___"+MotionPathNode+"___"+str(float(i)/self.InstancesNum))
					cmds.cutKey(MotionPathNode+".u",cl=1)
					cmds.setAttr(MotionPathNode+".u",float(i)/self.InstancesNum)
				# self.ArrayMesh=cmds.duplicate(self.ArrayMesh,ilf=1)[0]
				# try:
				# 	cmds.parent(self.ArrayMesh,self.ArrayGRP)
				# except:
				# 	pass
				# self.CurrentMesh=self.ArrayMesh
				#Calculate Instanced Attributes
				else:
					self.FinaltX=self.ConstantX+self.RelativeX*self.SizeX+self.ofst_msh_tX
					self.FinaltY=self.ConstantY+self.RelativeY*self.SizeY+self.ofst_msh_tY
					self.FinaltZ=self.ConstantZ+self.RelativeZ*self.SizeZ+self.ofst_msh_tZ
					self.FinalrX=self.ofst_msh_rX
					self.FinalrY=self.ofst_msh_rY
					self.FinalrZ=self.ofst_msh_rZ
					#Transform Instance
					cmds.move(self.FinaltX,self.FinaltY,self.FinaltZ,self.CurrentMesh,os=1,wd=1,r=1)
					cmds.rotate('{}deg'.format(self.FinalrX),'{}deg'.format(self.FinalrY),'{}deg'.format(self.FinalrZ),self.CurrentMesh,os=1,r=1)
					cmds.scale(self.ofst_msh_sX,self.ofst_msh_sY,self.ofst_msh_sZ,self.CurrentMesh,os=1,r=1)
			cmds.parent(self.ArrayGRP,self.ArrayMeshName)
MyWindow=ArrayCls()