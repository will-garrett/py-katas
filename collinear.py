import sys

def collinear(pts):
  if len(pts) < 3: # by definition always collinear
    return True
  # get initial vector of 1st segment
  (x0, y0), (x1, y1) = pts[0], pts[1]
  dx, dy = x1-x0, y1 - y0 # calculate initial slope
  for xi, yi in pts[2:]: # iterate through remaining points
    if (xi - x0) * dy != (yi - y0) * dx: # check if not same as initial slope
      return False  # deviation means failure
  return True # no fail == no slope change

def parse_points_from_args(args):
    """Parse command line arguments into list of (x, y) tuples"""
    if len(args) % 2 != 0:
        raise ValueError("Number of coordinates must be even (each point needs x and y)")
    
    points = []
    for i in range(0, len(args), 2):
        try:
            x = float(args[i])
            y = float(args[i + 1])
            points.append((x, y))
        except ValueError:
            raise ValueError(f"Invalid coordinate: {args[i]} or {args[i + 1]}")
    
    return points

def print_usage():
    """Print usage instructions"""
    print("Usage: uv run collinear.py <x1> <y1> <x2> <y2> <x3> <y3> ...")
    print("Example: uv run collinear.py 1 1 2 2 4 4 -10 -10")
    print("This would check if points (1,1), (2,2), (4,4), (-10,-10) are collinear.")
    print()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, show usage and run examples
        print_usage()
        print("Running examples:")
        example1 = [(1,1), (2,2), (4,4), (-10, -10)]
        print(f"Points: {example1}")
        print(f"Collinear: {collinear(example1)}")
        print()
        example2 = [(1,0), (2,0), (3,1)]
        print(f"Points: {example2}")
        print(f"Collinear: {collinear(example2)}")
    else:
        # Parse command line arguments
        try:
            points = parse_points_from_args(sys.argv[1:])
            if len(points) < 2:
                print("Error: At least 2 points (4 coordinates) are required.")
                print_usage()
            else:
                result = collinear(points)
                print(f"Points: {points}")
                print(f"Collinear: {result}")
        except ValueError as e:
            print(f"Error: {e}")
            print_usage()