Point(1) = {0, 0, 0, 1.0};
Point(2) = {1, 0, 0, 1.0};
Point(3) = {1, 1, 0, 1.0};
Point(4) = {0, 1, 0, 1.0};
Point(5) = {0.3333333333333, 0.3333333333333, 0, 1.0};
Point(6) = {0.66666666666666, 0.3333333333333, 0, 1.0};
Point(7) = {0.66666666666666, 0.66666666666666, 0, 1.0};
Point(8) = {0.3333333333333, 0.66666666666666, 0, 1.0};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 5};
Line Loop(1) = {1, 2, 3, 4};
Line Loop(2) = {5, 6, 7, 8};
Plane Surface(1) = {1,2};
Physical Line(9) = {2, 3, 4, 1, 6, 7, 8, 5};
Physical Surface(10) = {1};
