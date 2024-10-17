mesh_size = 0.006;

Point(1) = {0, 0, 0, 1.0};
Point(2) = {0.3, 0, 0, 1.0};
Point(3) = {2.7, 0, 0, 1.0};
Point(4) = {3, 0, 0, 1.0};
Point(5) = {3, 0.5, 0, 1.0};
Point(6) = {3, 0.8, 0, 1.0};
Point(7) = {2.7, 0.8, 0, 1.0};
Point(8) = {2.7, 0.5, 0, 1.0};
Point(9) = {0.3, 0.5, 0, 1.0};
Point(10) = {0.3, 0.8, 0, 1.0};
Point(11) = {0, 0.8, 0, 1.0};
Point(12) = {0, 0.5, 0, 1.0};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {5, 8};
Line(9) = {8, 9};
Line(10) = {9, 10};
Line(11) = {10, 11};
Line(12) = {11, 12};
Line(13) = {9, 12};
Line(14) = {12, 1};

Curve Loop(1) = {-13, 10, 11, 12};
Plane Surface(1) = {1};

Curve Loop(2) = {1, 2, 3, 4, 8, 9, 13, 14};
Plane Surface(2) = {2};

Curve Loop(3) = {-8, 5, 6, 7};
Plane Surface(3) = {3};

MeshSize{ PointsOf{ Surface{1, 2, 3}; } } = mesh_size;

Physical Curve("Inlet", 1) = {11};
Physical Curve("Outlet", 2) = {6};
Physical Curve("Wall", 3) = {1, 3, 4, 5, 7, 10, 12, 14};
Physical Curve("Current collector", 4) = {9};
Physical Curve("Membrane", 5) = {2};
Physical Surface("Domain", 5) = {2};
Physical Surface(6) = {1};
Physical Surface(7) = {3};
