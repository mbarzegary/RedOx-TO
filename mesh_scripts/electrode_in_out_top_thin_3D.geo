size = 0.05;

Point(1) = {0, 0, 0, size};
Point(2) = {3.0, 0, 0, size};
Point(3) = {3.0, 3.0, 0, size};
Point(4) = {0, 3.0, 0, size};
Point(5) = {0.3, 0.3, 0, size};
Point(6) = {2.7, 0.3, 0, size};
Point(7) = {2.7, 2.7, 0, size};
Point(8) = {0.3, 2.7, 0, size};
Point(9) = {0, 0, 0.5, size};
Point(91) = {0, 0.3, 0.5, size};
Point(92) = {0.3, 0, 0.5, size};
Point(10) = {3.0, 0, 0.5, size};
Point(11) = {3.0, 3.0, 0.5, size};
Point(111) = {3.0, 2.7, 0.5, size};
Point(112) = {2.7, 3.0, 0.5, size};
Point(12) = {0, 3.0, 0.5, size};
Point(13) = {0.3, 0.3, 0.5, size};
Point(14) = {2.7, 0.3, 0.5, size};
Point(15) = {2.7, 2.7, 0.5, size};
Point(16) = {0.3, 2.7, 0.5, size};
Point(90) = {0, 0, 0.8, size};
Point(910) = {0, 0.3, 0.8, size};
Point(920) = {0.3, 0, 0.8, size};
Point(130) = {0.3, 0.3, 0.8, size};
Point(110) = {3.0, 3.0, 0.8, size};
Point(1110) = {3.0, 2.7, 0.8, size};
Point(1120) = {2.7, 3.0, 0.8, size};
Point(150) = {2.7, 2.7, 0.8, size};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 5};
Line(9) = {1, 9};
Line(10) = {2, 10};
Line(11) = {3, 11};
Line(12) = {4, 12};
Line(13) = {9, 92};
Line(14) = {92, 10};
Line(15) = {10, 111};
Line(16) = {111, 11};
Line(17) = {11, 112};
Line(18) = {112, 12};
Line(19) = {12, 91};
Line(20) = {91, 9};
Line(21) = {92, 13};
Line(22) = {13, 91};
Line(23) = {112, 15};
Line(24) = {15, 111};
Line(25) = {13, 14};
Line(26) = {14, 15};
Line(27) = {15, 16};
Line(28) = {16, 13};
Line(29) = {111, 1110};
Line(30) = {15, 150};
Line(31) = {11, 110};
Line(32) = {112, 1120};
Line(33) = {150, 1120};
Line(34) = {1120, 110};
Line(35) = {110, 1110};
Line(36) = {1110, 150};
Line(37) = {92, 920};
Line(38) = {9, 90};
Line(39) = {13, 130};
Line(40) = {91, 910};
Line(41) = {910, 90};
Line(42) = {90, 920};
Line(43) = {920, 130};
Line(44) = {130, 910};

Curve Loop(1) = {1, 2, 3, 4, 5, 6, 7, 8};
Plane Surface(1) = {1};

Curve Loop(2) = {8, 5, 6, 7};
Plane Surface(2) = {2};

Curve Loop(3) = {1, 10, -14, -13, -9};
Plane Surface(3) = {3};

Curve Loop(4) = {2, 11, -16, -15, -10};
Plane Surface(4) = {4};

Curve Loop(5) = {3, 12, -18, -17, -11};
Plane Surface(5) = {5};

Curve Loop(6) = {9, -20, -19, -12, 4};
Plane Surface(6) = {6};

Curve Loop(7) = {21, 25, 26, 24, -15, -14};
Plane Surface(7) = {7};

Curve Loop(8) = {18, 19, -22, -28, -27, -23};
Plane Surface(8) = {8};

Curve Loop(9) = {25, 26, 27, 28};
Plane Surface(9) = {9};

Curve Loop(10) = {13, 21, 22, 20};
Plane Surface(10) = {10};

Curve Loop(11) = {24, 16, 17, 23};
Plane Surface(11) = {11};

Curve Loop(12) = {37, -42, -38, 13};
Plane Surface(12) = {12};

Curve Loop(13) = {21, 39, -43, -37};
Plane Surface(13) = {13};

Curve Loop(14) = {39, 44, -40, -22};
Plane Surface(14) = {14};

Curve Loop(15) = {41, -38, -20, 40};
Plane Surface(15) = {15};

Curve Loop(16) = {42, 43, 44, 41};
Plane Surface(16) = {16};

Curve Loop(17) = {24, 29, 36, -30};
Plane Surface(17) = {17};

Curve Loop(18) = {29, -35, -31, -16};
Plane Surface(18) = {18};

Curve Loop(19) = {34, -31, 17, 32};
Plane Surface(19) = {19};

Curve Loop(20) = {33, -32, 23, 30};
Plane Surface(20) = {20};

Curve Loop(21) = {36, 33, 34, 35};
Plane Surface(21) = {21};

Surface Loop(1) = {12, 13, 14, 16, 15, 10};
Volume(1) = {1};

Surface Loop(2) = {21, 17, 18, 19, 20, 11};
Volume(2) = {2};

Surface Loop(3) = {9, 7, 4, 1, 3, 6, 8, 5, 2, 10, 11};
Volume(3) = {3};

Physical Volume("Domain", 5) = {3};
Physical Volume("Inlet", 6) = {1};
Physical Volume("Outlet", 7) = {2};

Physical Surface("Inlet", 1) = {16};
Physical Surface("Outlet", 2) = {21};
Physical Surface("Current collector", 4) = {9};
Physical Surface("Membrane", 5) = {2};
Physical Surface("Wall", 3) = {14, 12, 15, 13, 3, 8, 1, 4, 5, 6, 7, 17, 20, 19, 18};
