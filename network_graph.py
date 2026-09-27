"""Stop adjacency for transit lines drawn as PDF polylines.

Used by server.py, resources/export_static.py and the PDF reconciliation
scripts. Given a line's route segments (`path_json`) and its ordered stop
positions, `line_edges` returns which stops are neighbours along the drawn
geometry, handling branches, loops, junctions and small drawing gaps.
"""

from __future__ import annotations

import heapq
import math
from collections import defaultdict


def project(point, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, ((point[0] - ax) * dx + (point[1] - ay) * dy) / length2))
    px, py = ax + t * dx, ay + t * dy
    return math.hypot(point[0] - px, point[1] - py), (px, py), t


def polyline_nearest(point, points):
    """(distance, projected point, distance along the polyline)."""
    best = (float("inf"), None, 0.0)
    walked = 0.0
    for a, b in zip(points, points[1:]):
        dist, proj, t = project(point, a, b)
        seg = math.dist(a, b)
        if dist < best[0]:
            best = (dist, proj, walked + t * seg)
        walked += seg
    return best


def locate_stops(segments, positions):
    """Attach each (x, y) to its nearest segment: dicts with chain/along."""
    chains = [[tuple(p) for p in seg] for seg in segments if len(seg) > 1]
    stops = []
    for x, y in positions:
        hits = sorted(
            (polyline_nearest((x, y), c) + (ci,) for ci, c in enumerate(chains)),
            key=lambda v: v[0],
        )
        if not hits:
            stops.append({"x": x, "y": y, "chain": 0, "along": 0.0})
            continue
        best = hits[0]
        # Junction stations lie on several chains of the same line.
        locations = [(h[3], h[2]) for h in hits if h[0] <= min(best[0] + 4.0, 12.0)]
        stops.append({"x": x, "y": y, "chain": best[3], "along": best[2], "locations": locations})
    return chains, stops


def line_edges(chains, stops, tol=7.0, bridge=80.0, extra=()):
    """Adjacent stop pairs (index pairs into stops) following the geometry.

    Builds a graph of chain endpoints, junctions and stops, then walks from
    every stop to the next stops reachable without passing another stop.
    Remaining disconnected parts are bridged by their closest stop pair when
    closer than `bridge` (pieces broken at capsules or drawn with gaps).
    """
    parent = {}

    def find(k):
        parent.setdefault(k, k)
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    def union(a, b):
        parent[find(a)] = find(b)

    lengths = [sum(math.dist(p, q) for p, q in zip(c, c[1:])) for c in chains]
    events = defaultdict(list)  # chain -> [(along, node)]
    for ci, chain in enumerate(chains):
        events[ci].append((0.0, ("E", ci, 0)))
        events[ci].append((lengths[ci], ("E", ci, 1)))
    for ci, chain in enumerate(chains):
        for end, point in ((0, chain[0]), (1, chain[-1])):
            for cj, other in enumerate(chains):
                if cj == ci:
                    continue
                dist, _, along = polyline_nearest(point, other)
                if dist <= tol:
                    events[cj].append((along, ("E", ci, end)))
            for cj in range(len(chains)):
                for end2, point2 in ((0, chains[cj][0]), (1, chains[cj][-1])):
                    if (cj, end2) != (ci, end) and math.dist(point, point2) <= tol:
                        union(("E", ci, end), ("E", cj, end2))
    for i, stop in enumerate(stops):
        for chain, along in stop.get("locations") or [(stop["chain"], stop["along"])]:
            if chain < len(chains):
                events[chain].append((along, ("S", i)))

    graph = defaultdict(list)
    for ci, evs in events.items():
        evs.sort(key=lambda e: e[0])
        for (a1, n1), (a2, n2) in zip(evs, evs[1:]):
            k1 = find(n1) if n1[0] == "E" else n1
            k2 = find(n2) if n2[0] == "E" else n2
            if k1 == k2:
                continue
            w = max(a2 - a1, 0.01)
            graph[k1].append((k2, w))
            graph[k2].append((k1, w))

    edges = {}
    for i in range(len(stops)):
        start = ("S", i)
        best = {start: 0.0}
        heap = [(0.0, start)]
        while heap:
            d, node = heapq.heappop(heap)
            if d > best.get(node, float("inf")):
                continue
            if node[0] == "S" and node != start:
                j = node[1]
                key = (min(i, j), max(i, j))
                edges[key] = min(edges.get(key, float("inf")), d)
                continue
            for nxt, w in graph.get(node, ()):
                nd = d + w
                if nd < best.get(nxt, float("inf")):
                    best[nxt] = nd
                    heapq.heappush(heap, (nd, nxt))

    for a, b in extra:
        edges[(min(a, b), max(a, b))] = math.dist((stops[a]["x"], stops[a]["y"]), (stops[b]["x"], stops[b]["y"]))

    # Bridge small gaps between disconnected parts.
    while True:
        comp = {}
        uf = list(range(len(stops)))

        def f(k):
            while uf[k] != k:
                uf[k] = uf[uf[k]]
                k = uf[k]
            return k

        for (a, b) in edges:
            uf[f(a)] = f(b)
        roots = {f(k) for k in range(len(stops))}
        if len(roots) <= 1:
            break
        best = None
        for a in range(len(stops)):
            for b in range(a + 1, len(stops)):
                if f(a) == f(b):
                    continue
                d = math.dist((stops[a]["x"], stops[a]["y"]), (stops[b]["x"], stops[b]["y"]))
                if best is None or d < best[0]:
                    best = (d, a, b)
        if best is None or best[0] > bridge:
            break
        edges[(best[1], best[2])] = best[0]
    return sorted((a, b, w) for (a, b), w in prune_redundant(edges, keep=set(extra)).items())


def prune_redundant(edges, keep=()):
    """Remove edges bypassing intermediate stops (from overlapping pieces).

    An edge a-b is redundant when a path a..b through other stops is at most
    12% longer: the drawn line visits those stops on the way.
    """
    edges = dict(edges)
    keep = {(min(a, b), max(a, b)) for a, b in keep}
    for key in sorted(edges, key=lambda k: -edges[k]):
        if key in keep or key not in edges:
            continue
        a, b = key
        w = edges[key]
        graph = defaultdict(list)
        for (x, y), ww in edges.items():
            if (x, y) == key:
                continue
            graph[x].append((y, ww))
            graph[y].append((x, ww))
        best = {a: 0.0}
        heap = [(0.0, a)]
        limit = w * 1.12 + 3
        found = False
        while heap:
            d, node = heapq.heappop(heap)
            if d > limit:
                break
            if node == b:
                found = True
                break
            if d > best.get(node, float("inf")):
                continue
            for nxt, ww in graph[node]:
                nd = d + ww
                if nd < best.get(nxt, float("inf")):
                    best[nxt] = nd
                    heapq.heappush(heap, (nd, nxt))
        if found:
            del edges[key]
    return edges


def components(n, edges):
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b in edges:
        parent[find(a)] = find(b)
    return len({find(i) for i in range(n)})


def order_stations(ids, edges, first=None):
    """Readable station order for a line: the longest terminus-to-terminus
    path first (starting at `first` when it is one of its ends), then each
    branch, walked outward from where it joins the stations already listed."""
    graph = defaultdict(list)
    for a, b, w in edges:
        graph[a].append((b, w))
        graph[b].append((a, w))

    def shortest(src):
        best = {src: 0.0}
        prev = {}
        heap = [(0.0, src)]
        while heap:
            d, node = heapq.heappop(heap)
            if d > best.get(node, float("inf")):
                continue
            for nxt, w in graph[node]:
                nd = d + w
                if nd < best.get(nxt, float("inf")):
                    best[nxt] = nd
                    prev[nxt] = node
                    heapq.heappush(heap, (nd, nxt))
        return best, prev

    ids = list(ids)
    if len(ids) < 2 or not edges:
        return ids
    termini = [i for i in ids if len(graph[i]) <= 1] or ids[:1]
    best_pair = None
    for t in termini:
        dist, prev = shortest(t)
        for u, d in dist.items():
            if u in termini and (best_pair is None or d > best_pair[0]):
                best_pair = (d, t, u, prev)
    if best_pair is None:
        return ids
    _, start, end, prev = best_pair
    if first is not None and first == end:
        start, end = end, start
        _, prev = shortest(start)
    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    order = path[::-1]
    seen = set(order)
    while len(seen) < len(ids):
        rank = {sid: i for i, sid in enumerate(order)}
        candidates = [
            (rank[v], u) for u in ids if u not in seen for v, _ in graph[u] if v in seen
        ]
        if not candidates:
            order.extend(i for i in ids if i not in seen)
            break
        _, root = min(candidates)
        # Walk the branch outward, farthest unvisited end first.
        dist, prev_b = shortest(root)
        reachable = [u for u in dist if u not in seen]
        far = max(reachable, key=lambda u: dist[u])
        branch = [far]
        while branch[-1] != root:
            branch.append(prev_b[branch[-1]])
        branch = [u for u in branch[::-1] if u not in seen]
        order.extend(branch)
        seen.update(branch)
    return order
