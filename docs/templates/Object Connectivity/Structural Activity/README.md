Structural Activity
===================

Structural activities may be linked to structural items.

```
concept {
    IfcStructuralActivity:AppliedLoad -> IfcStructuralLoad
    IfcStructuralActivity:AssignedToStructuralItem -> IfcRelConnectsStructuralActivity:RelatedStructuralActivity
    IfcRelConnectsStructuralActivity:RelatingElement -> IfcStructuralItem
}
```
