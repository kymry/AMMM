/*********************************************
 * Authors: Jerome Pasvantis and Kymry Burwell
 *********************************************/

 int minHours = ...;
 int maxHours = ...;
 int maxConsec = ...;
 int maxPresence = ...;
 int nNurses = ...;
 int hours = ...;
 int M = hours; //Big Number

 range N = 1..nNurses;
 range H = 1..hours;
 range C = 0..maxConsec;

 int demand[h in H] = ...;

 dvar boolean worksToday[n in N];
 dvar boolean working[n in N, h in H];
 dvar boolean worksBefore[n in N, h in H];
 dvar boolean worksAfter[n in N, h in H];

// Objective: Minimize the number of nurses that work
minimize sum(n in N) worksToday[n];

subject to{
// Constraint 0: If nurse is working today -> set worksToday to true
forall(n in N)
  worksToday[n] * M >= sum(h in H) working[n, h];

// Constraint 1: Demand of nurses for each hour is met
forall(h in H)
  (sum(n in N) working[n, h]) >= demand[h];

// Constraint 2: All working nurses work at least minHours
forall(n in N)
  (sum(h in H) working[n,h]) >= minHours * worksToday[n];

// Constraing 3: All working nurses work at most maxHours
forall(n in N)
  (sum(h in H) working[n,h]) <= maxHours * worksToday[n];

// Constraint 4: All working nurses work at most maxConsec consecutive hours
forall(n in N, h in H: h <= hours - maxConsec)
  (sum(c in C) working[n, h+c]) <= maxConsec;

// Constraint 5: All working nurses should not stay longer than maxPresence
forall(n in N)
  (sum(h in H) worksAfter[n,h]) - (hours - sum(h in H) worksBefore[n,h]) <= maxPresence -2;

// Constraint 6: No working nurse can rest for more than two consecutive hours
forall(n in N, h in H: h < hours)
  working[n,h] + working[n,h+1] >= worksBefore[n,h] + worksAfter[n,h] - 1;

// Constraint 6a/Helper: worksBefore is true if nurse worked before that hour
forall(n in N, h in H)
  worksBefore[n, h] * M >= (sum(h2 in H: h2 < h) working[n, h2]);
// Otherwise false
forall(n in N, h in H)
  worksBefore[n,h] <= (sum(h2 in H: h2 < h) working[n, h2]);

// Constraint 6b/Helper: worksAfter is true if nurse
forall(n in N, h in H)
  worksAfter[n,h] * M >= (sum(h2 in H: h2 > h) working[n, h2]);
// Otherwise false
forall(n in N, h in H)
  worksAfter[n,h] <= (sum(h2 in H: h2 > h) working[n, h2]);


}
