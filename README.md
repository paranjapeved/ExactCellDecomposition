## A Robot Motion Planning Project 
## By: Ved Paranjape

### I implemented my own exact cell decomposition algorithm using plain python without incorporating any 3rd party motion planning libraries. It was implemented using concepts from Computational Geometry for collision checking. For simulation of the environment and for graphics, the python pygame library was used. The following is a summary of the project details and some specifics of the implementation aspects.

## Introduction
### Exact Cell Decomposition divides the workspace into multiple connected units (cells) which are trapezoidal in shape as shown in the following figure. 

![](https://github.com/paranjapeved/ExactCellDecomposition/blob/master/Images/Basic.png)

### These trapezoids are constructed by sweeping a vertical line from the minimum x to the maximum x coordinate of the workspace. Whenever the sweep line reaches a vertex (outer boundary vertex or an obstacle vertex), the points of intersection of the line with the all the edges of the environment are found out. This is done with the help of computational geometry algorithm for finding out the point of intersection of a line. The format of the line for this purpose has been tweaked into a homogeneous slope intercept format as follows:

## [slope, -1, y-intercept]

### This list is used to compute the point of intersection. The two endpoints of the two lines for which the point of intersection is to be found are passed as arguments to the function point_of_intersection(). To convert the line to the homogeneous format, the two endpoints of the line such as [a,b] and [c,d] for a line ab-cd are passed to the do-edge-equation() function. 

#### The code is hosted on my github (Please click the "View on Github" button).

## Structure
### The code consists of 3 classes: Environment




