Body SweptSolid PolyCurve Geometry
==================================

The _Body SweptSolid PolyCurve Geometry_ is the representation of the 3D shape of a product by swept solid models, only allowing for the basic extruded area solids and revolved area solids.

The following attribute values for the _IfcShapeRepresentation_ holding this geometric representation shall be used:

* _IfcShapeRepresentation_._RepresentationIdentifier_ = 'Body'
* _IfcShapeRepresentation_._RepresentationType_ = 'SweptSolid'
* _IfcShapeRepresentation_._Items_ = _IfcExtrudedAreaSolid_, _IfcRevolvedAreaSolid_
* _IfcShapeRepresentation_._Items[1..n].SweptArea_ = _IfcArbitraryClosedProfileDef_, _IfcArbitraryProfileDefWithVoids_
* _IfcShapeRepresentation_._Items[1..n].SweptArea.OuterCurve_ = _IfcIndexedPolyCurve_
* _IfcShapeRepresentation_._Items[1..n].SweptArea.InnerCurves_ = _IfcIndexedPolyCurve_

```
concept {
    IfcElement:Representation -> IfcProductDefinitionShape
    IfcProductDefinitionShape:Representations -> IfcShapeRepresentation
    IfcShapeRepresentation:ContextOfItems -> IfcGeometricRepresentationContext
    IfcShapeRepresentation:RepresentationIdentifier -> IfcLabel
    IfcShapeRepresentation:RepresentationType -> IfcLabel
    IfcShapeRepresentation:Items -> IfcSweptAreaSolid
}
```
