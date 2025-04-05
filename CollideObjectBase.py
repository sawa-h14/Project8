from panda3d.core import PandaNode, Loader, NodePath, CollisionNode, CollisionSphere, CollisionInvSphere, CollisionCapsule, Vec3, BitMask32


class PlacedObject(PandaNode):
    # Just a generic object in the scene at this point. No relation to collisions.
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):
        self.modelNode : NodePath = loader.loadModel(modelPath)

        # We want to make sure we are having the right type passed to this parameter, or else throw an error.
        if not isinstance(self.modelNode, NodePath):
            raise AssertionError("PlacedObject loader.loadModel(" + modelPath + ") did not return a proper PandaNode!")
        
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setName(nodeName)
    
class CollidableObject(PlacedObject):
    # Now, we relate our PlacedObject to collisions by using it as a helper class for this function to create collisions.
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):
        super(CollidableObject, self).__init__(loader, modelPath, parentNode, nodeName)
        # Every single type of collider will get the "_cNode" tag behind it to signify that it's a collidable object.
        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + '_cNode'))
        #self.collisionNode.show()

class SphereCollideObject(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius: float, isPlayer: bool = False, isMissile: bool = False):
        super(SphereCollideObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(CollisionSphere(colPositionVec, colRadius))

        if isPlayer:
            self.collisionNode.setCollideMask(BitMask32.bit(2) | BitMask32.bit(3)) # Detects collisions

        elif isMissile:
            self.collisionNode.node().setFromCollideMask(BitMask32.bit(1)) # Detects collisions
            self.collisionNode.node().setIntoCollideMask(BitMask32.bit(1)) # Detects collisions
        else:
            self.collisionNode.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2) | BitMask32.bit(3))
        # self.collisionNode.show()

class InverseSphereCollideObject(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius: float):
        super(InverseSphereCollideObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(CollisionInvSphere(colPositionVec, colRadius))
        self.collisionNode.setCollideMask(BitMask32.bit(1)| BitMask32.bit(2) | BitMask32.bit(3))
        #self.collisionNode.show()

class CapsuleCollidableObject(CollidableObject):
    # a and b are representively the furthest point on a capsule collider on either side.
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, ax: float, ay: float, az: float, bx: float, by: float, bz: float, r: float):
        super(CapsuleCollidableObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(CollisionCapsule(ax, ay, az, bx, by, bz, r))
        self.collisionNode.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2) | BitMask32.bit(3))
        # self.collisionNode.show()

