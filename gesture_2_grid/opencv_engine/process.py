import cv2
import numpy as np
import sys
import json
import math

# ----------------------------
# Helper: line intersection
# ----------------------------
def intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(denom) < 1e-6:
        return None

    px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / denom

    return [int(px), int(py)]


# ----------------------------
# Helper: cluster points (simple K-means)
# ----------------------------
def kmeans(points, k=2, iterations=10):
    if len(points) < k:
        return points

    centers = points[:k]

    for _ in range(iterations):
        clusters = [[] for _ in range(k)]

        for p in points:
            dists = [np.linalg.norm(np.array(p)-np.array(c)) for c in centers]
            idx = np.argmin(dists)
            clusters[idx].append(p)

        new_centers = []
        for cluster in clusters:
            if cluster:
                new_centers.append(np.mean(cluster, axis=0))
            else:
                new_centers.append(centers[len(new_centers)])

        centers = new_centers

    return [list(map(int, c)) for c in centers]


# ----------------------------
# Detect straight lines
# ----------------------------
def detect_lines(edges):
    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=80,
        minLineLength=40,
        maxLineGap=10
    )

    result = []
    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = l[0]
            result.append([x1, y1, x2, y2])

    return result


# ----------------------------
# Detect curves → convert to lines
# ----------------------------
def detect_curves(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    curve_lines = []

    for cnt in contours:
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Convert curve into segments
        for i in range(len(approx) - 1):
            x1, y1 = approx[i][0]
            x2, y2 = approx[i + 1][0]

            curve_lines.append([x1, y1, x2, y2])

    return curve_lines


# ----------------------------
# Compute vanishing points
# ----------------------------
def compute_vanishing_points(lines):
    intersections = []

    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            p = intersection(lines[i], lines[j])
            if p:
                intersections.append(p)

    if len(intersections) < 2:
        return []

    # Auto detect perspective type
    k = min(3, max(1, len(intersections)//20))

    vps = kmeans(intersections, k=k)

    return vps


# ----------------------------
# MAIN
# ----------------------------
def main():
    img_path = sys.argv[1]
    output_path = sys.argv[2]

    img = cv2.imread(img_path)

    # Resize for speed
    scale = 0.5
    img = cv2.resize(img, (0,0), fx=scale, fy=scale)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Detect lines
    lines = detect_lines(edges)

    # Detect curves and convert
    curve_lines = detect_curves(edges)

    all_lines = lines + curve_lines

    # Compute vanishing points
    vps = compute_vanishing_points(all_lines)

    # Scale back results
    def upscale(line):
        return [int(v/scale) for v in line]

    all_lines = [upscale(l) for l in all_lines]
    vps = [upscale(v) for v in vps]

    result = {
        "lines": all_lines,
        "vanishing_points": vps
    }

    with open(output_path, "w") as f:
        json.dump(result, f)


if __name__ == "__main__":
    main()
